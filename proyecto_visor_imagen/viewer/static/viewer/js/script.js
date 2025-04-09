document.addEventListener('DOMContentLoaded', function() {
  // Elements
  const previewImage = document.getElementById('previewImage');
  const histogramCanvas = document.getElementById('histogramCanvas');
  const filterOptions = document.querySelectorAll('.filter-option');
  const resetBtn = document.getElementById('resetBtn');
  const saveImageBtn = document.querySelector('.bg-sky-600');
  
  // State variables
  let originalImageData = null;
  let currentImageData = null;
  let currentFilter = null;
  let histogramChart = null;
  
  // Initialize home page file upload if it exists
  const uploadContainer = document.getElementById('uploadContainer');
  const fileInput = document.getElementById('fileInput');
  
  if (uploadContainer && fileInput) {
      // Home page initialization
      initializeHomePageUpload();
  }
  
  // Initialize editor page if preview image exists
  if (previewImage) {
      console.log("Preview image element found");
      
      // Get stored image data from sessionStorage (when navigating from home)
      const storedImageData = sessionStorage.getItem('originalImage');
      console.log("Stored image data:", storedImageData ? "Found" : "Not found");
      
      if (storedImageData) {
          console.log("Loading image to editor");
          loadImageToEditor(storedImageData);
      } else {
          // For testing, load a placeholder image
          console.log("No stored image found, loading placeholder");
          previewImage.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==";
      }
      
      // Initialize filter options
      initializeFilterOptions();
      
      // Initialize reset button
      if (resetBtn) {
          resetBtn.addEventListener('click', function() {
              resetToOriginalImage();
          });
      }
      
      // Initialize refresh histogram button
      const refreshHistogramBtn = document.getElementById('refreshHistogramBtn');
      if (refreshHistogramBtn) {
          refreshHistogramBtn.addEventListener('click', function() {
              // Mostrar un indicador de carga en el botón
              const originalText = refreshHistogramBtn.innerHTML;
              refreshHistogramBtn.innerHTML = `
                  <svg class="animate-spin h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Refreshing...
              `;
              
              // Generar el histograma con la imagen actual
              if (currentImageData) {
                  console.log("Refreshing histogram manually");
                  generateHistogram(currentImageData)
                      .then(() => {
                          // Restaurar el texto original del botón
                          refreshHistogramBtn.innerHTML = originalText;
                      })
                      .catch(error => {
                          console.error("Error refreshing histogram:", error);
                          refreshHistogramBtn.innerHTML = originalText;
                      });
              } else {
                  console.warn("No image data available for histogram");
                  refreshHistogramBtn.innerHTML = originalText;
              }
          });
      }
      
      // Initialize save image button
      const downloadBtn = document.getElementById('downloadBtn');
      if (downloadBtn) {
          downloadBtn.addEventListener('click', function() {
              downloadProcessedImage();
          });
      }
  }
  
  // ========== Functions ==========
  
  function initializeHomePageUpload() {
      // File upload handling
      uploadContainer.addEventListener('dragover', function(e) {
          e.preventDefault();
          this.classList.add('drag-over');
      });
      
      uploadContainer.addEventListener('dragleave', function() {
          this.classList.remove('drag-over');
      });
      
      uploadContainer.addEventListener('drop', function(e) {
          e.preventDefault();
          this.classList.remove('drag-over');
          if (e.dataTransfer.files.length) {
              handleFileUpload(e.dataTransfer.files[0]);
          }
      });
      
      uploadContainer.addEventListener('click', function() {
          fileInput.click();
      });
      
      fileInput.addEventListener('change', function() {
          if (this.files.length) {
              handleFileUpload(this.files[0]);
          }
      });
  }
  
  function handleFileUpload(file) {
      if (!file.type.match('image.*')) {
          alert('Please upload an image file');
          return;
      }
      
      const reader = new FileReader();
      reader.onload = function(e) {
          // Store image data in localStorage and redirect to editor
          localStorage.setItem('uploadedImageData', e.target.result);
          window.location.href = '/editor/';
      };
      reader.readAsDataURL(file);
  }
  
  function loadImageToEditor(imageData) {
      console.log("Loading image to editor...");
      
      // Set preview image and store original data
      previewImage.src = imageData;
      originalImageData = imageData;
      currentImageData = imageData;
      
      // Store in hidden inputs for form submission if needed
      const originalDataInput = document.getElementById('originalImageData');
      const currentDataInput = document.getElementById('currentImageData');
      
      if (originalDataInput) originalDataInput.value = imageData;
      if (currentDataInput) currentDataInput.value = imageData;
      
      // Generate histogram when image is loaded
      previewImage.onload = function() {
          console.log("Image loaded successfully");
          generateHistogram(imageData)
              .then(() => console.log("Histogram generated successfully"))
              .catch(error => console.error("Error generating histogram:", error));
      };
      
      // Handle image load error
      previewImage.onerror = function() {
          console.error("Error loading image");
          alert("Error loading image. Please try again.");
      };
  }
  
  function initializeFilterOptions() {
      // Add click event listeners to filter options
      filterOptions.forEach(option => {
          option.addEventListener('click', function() {
              const filterType = this.getAttribute('data-filter');
              
              // Remove active class from all options
              filterOptions.forEach(opt => opt.classList.remove('active'));
              
              // Add active class to selected option
              this.classList.add('active');
              
              // Set current filter
              currentFilter = filterType;
              
              // Show filter controls based on filter type
              showFilterControls(filterType);
          });
      });
  }
  
  function showFilterControls(filterType) {
      // Hide all predefined filter controls
      const predefinedControls = document.querySelectorAll('.filter-controls');
      predefinedControls.forEach(control => {
          control.classList.add('hidden');
      });
      
      // Special case for 4mosaic
      if (filterType === '4mosaic') {
          const mosaicControl = document.getElementById('fourMosaicControls');
          if (mosaicControl) {
              mosaicControl.classList.remove('hidden');
              
              // Initialize the mosaic control
              initializeMosaicControl();
              
              // Set the current image preview
              const currentImagePreview = document.getElementById('currentImagePreview');
              if (currentImagePreview && currentImageData) {
                  currentImagePreview.src = currentImageData;
              }
              
              return;
          }
      }
      
      // Special case for merge
      if (filterType === 'merge') {
          const mergeControl = document.getElementById('mergeControls');
          if (mergeControl) {
              mergeControl.classList.remove('hidden');
              
              // Initialize the merge control
              initializeMergeControl();
              return;
          }
      }
      
      // Remove any existing dynamic filter control elements
      const existingControls = document.getElementById('filterControls');
      if (existingControls) {
          existingControls.remove();
      }
      
      // Create filter controls container
      const controlsContainer = document.createElement('div');
      controlsContainer.id = 'filterControls';
      controlsContainer.className = 'mt-4 bg-gray-800 rounded-md p-3';
      
      // Add different controls based on filter type
      switch (filterType) {
          case 'brightness':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="slider-label">
                          <span>Brightness</span>
                          <span id="brightnessValue">1.0</span>
                      </div>
                      <input type="range" id="brightnessSlider" min="0" max="2" step="0.1" value="1.0">
                  </div>
                  <button id="applyBrightnessBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'contrast':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="slider-label">
                          <span>Contrast</span>
                          <span id="contrastValue">1.0</span>
                      </div>
                      <input type="range" id="contrastSlider" min="0" max="2" step="0.1" value="1.0">
                  </div>
                  <button id="applyContrastBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'rotate':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="slider-label">
                          <span>Angle (degrees)</span>
                          <span id="rotationValue">0°</span>
                      </div>
                      <input type="range" id="rotationSlider" min="0" max="360" step="15" value="0">
                  </div>
                  <button id="applyRotationBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'zoom':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="slider-label">
                          <span>Zoom level</span>
                          <span id="zoomValue">1.0x</span>
                      </div>
                      <input type="range" id="zoomSlider" min="1" max="5" step="0.1" value="1.0">
                  </div>
                  <p class="text-sm text-gray-400 mb-3">Zoom will be applied to the center of the image</p>
                  <button id="applyZoomBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'rgb':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="checkbox-container">
                          <input type="checkbox" id="redChannel" checked>
                          <label for="redChannel" class="text-red-500">Red Channel</label>
                      </div>
                      <div class="checkbox-container">
                          <input type="checkbox" id="greenChannel" checked>
                          <label for="greenChannel" class="text-green-500">Green Channel</label>
                      </div>
                      <div class="checkbox-container">
                          <input type="checkbox" id="blueChannel" checked>
                          <label for="blueChannel" class="text-blue-500">Blue Channel</label>
                      </div>
                  </div>
                  <button id="applyRGBBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'cmy':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="checkbox-container">
                          <input type="checkbox" id="cyanChannel" checked>
                          <label for="cyanChannel" class="text-cyan-500">Cyan Channel</label>
                      </div>
                      <div class="checkbox-container">
                          <input type="checkbox" id="magentaChannel" checked>
                          <label for="magentaChannel" class="text-pink-500">Magenta Channel</label>
                      </div>
                      <div class="checkbox-container">
                          <input type="checkbox" id="yellowChannel" checked>
                          <label for="yellowChannel" class="text-yellow-500">Yellow Channel</label>
                      </div>
                  </div>
                  <button id="applyCMYBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'highlight':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="flex flex-col space-y-2">
                          <label class="flex items-center">
                              <input type="radio" name="highlightMode" value="light" checked>
                              <span class="ml-2">Highlight Light Areas</span>
                          </label>
                          <label class="flex items-center">
                              <input type="radio" name="highlightMode" value="dark">
                              <span class="ml-2">Highlight Dark Areas</span>
                          </label>
                          <label class="flex items-center">
                              <input type="radio" name="highlightMode" value="midtones">
                              <span class="ml-2">Highlight Midtones</span>
                          </label>
                      </div>
                  </div>
                  <button id="applyHighlightBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'negative':
              controlsContainer.innerHTML = `
                  <p class="text-sm text-gray-400 mb-3">Invert all colors in the image</p>
                  <button id="applyNegativeBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply Negative Filter</button>
              `;
              break;
              
          case 'binary':
              controlsContainer.innerHTML = `
                  <div class="mb-3">
                      <div class="slider-label">
                          <span>Threshold</span>
                          <span id="thresholdValue">128</span>
                      </div>
                      <input type="range" id="thresholdSlider" min="0" max="255" step="1" value="128">
                  </div>
                  <button id="applyBinaryBtn" class="w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded">Apply</button>
              `;
              break;
              
          case 'merge':
              controlsContainer.innerHTML = `
                  <h3 class="text-md font-semibold mb-3">Merge Images</h3>
                  <p class="text-sm mb-3">Upload a second image to merge with the current one.</p>
                  
                  <!-- Second Image Upload -->
                  <div class="mb-3">
                      <label class="block text-sm mb-1">Second Image:</label>
                      <div class="flex items-center">
                          <input type="file" id="secondImage" class="hidden" accept="image/jpeg, image/png">
                          <button id="selectSecondImageBtn" class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm mr-2">
                              Select Image
                          </button>
                          <span id="secondImageName" class="text-sm text-gray-400">No image selected</span>
                      </div>
                      <div id="secondImagePreview" class="mt-2 hidden">
                          <img id="secondImagePreviewImg" class="max-h-32 max-w-full object-contain border border-gray-700 rounded" alt="Second Image Preview">
                      </div>
                  </div>
                  
                  <!-- Merge Type Selection -->
                  <div class="mb-3">
                      <label class="block text-sm mb-1">Merge Type:</label>
                      <div class="grid grid-cols-2 gap-2">
                          <label class="flex items-center p-2 border border-gray-700 rounded cursor-pointer hover:bg-gray-800">
                              <input type="radio" name="mergeType" value="alpha" class="mr-2" checked>
                              <span>Alpha Blend</span>
                          </label>
                          <label class="flex items-center p-2 border border-gray-700 rounded cursor-pointer hover:bg-gray-800">
                              <input type="radio" name="mergeType" value="watermark" class="mr-2">
                              <span>Watermark</span>
                          </label>
                      </div>
                  </div>
                  
                  <!-- Alpha Slider (only for alpha blend) -->
                  <div id="alphaSliderContainer" class="slider-container mb-2">
                      <label class="block text-sm mb-1">Blend Ratio: <span id="alphaValue">0.5</span></label>
                      <input type="range" id="alphaSlider" min="0" max="1" step="0.1" value="0.5" class="w-full">
                  </div>
                  
                  <button id="applyMergeBtn" class="w-full mt-2 py-2 bg-sky-600 hover:bg-sky-700 rounded">Apply Merge</button>
              `;
              break;
              
          default:
              controlsContainer.innerHTML = `
                  <p class="text-gray-400">Select a filter option to continue</p>
              `;
      }
      
      // Add the controls container after the filter options
      document.querySelector('.bg-gray-900.rounded-lg.p-4').appendChild(controlsContainer);
      
      // Add event listeners to the controls
      addControlEventListeners(filterType);
  }
  
  // Función para inicializar el control de mosaico
  function initializeMosaicControl() {
      console.log("Initializing mosaic control");
      
      // Elementos del DOM
      const applyMosaicBtn = document.getElementById('applyMosaic');
      const currentImagePreview = document.getElementById('currentImagePreview');
      const frameSizeSlider = document.getElementById('frameSizeSlider');
      const frameSizeValue = document.getElementById('frameSizeValue');
      const frameColorRadios = document.getElementsByName('frameColor');
      
      // Elementos para las imágenes adicionales
      const image1Input = document.getElementById('image1Input');
      const image2Input = document.getElementById('image2Input');
      const image3Input = document.getElementById('image3Input');
      const selectImage1Btn = document.getElementById('selectImage1Btn');
      const selectImage2Btn = document.getElementById('selectImage2Btn');
      const selectImage3Btn = document.getElementById('selectImage3Btn');
      const image1Preview = document.getElementById('image1Preview');
      const image2Preview = document.getElementById('image2Preview');
      const image3Preview = document.getElementById('image3Preview');
      
      // Variables para almacenar los datos de las imágenes
      let image1Data = null;
      let image2Data = null;
      let image3Data = null;
      
      // Mostrar la imagen actual en la vista previa
      if (currentImagePreview && currentImageData) {
          console.log("Setting current image preview");
          currentImagePreview.src = currentImageData;
      }
      
      // Actualizar el valor del tamaño del marco
      if (frameSizeSlider && frameSizeValue) {
          frameSizeSlider.addEventListener('input', function() {
              frameSizeValue.textContent = this.value;
          });
      }
      
      // Función para manejar la selección de imágenes
      const setupImageUpload = (inputElement, selectButton, previewContainer, imageIndex) => {
          if (selectButton && inputElement) {
              selectButton.addEventListener('click', function() {
                  inputElement.click();
              });
          }
          
          if (inputElement && previewContainer) {
              inputElement.addEventListener('change', function() {
                  if (this.files && this.files[0]) {
                      const file = this.files[0];
                      
                      // Validar tipo de archivo
                      if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
                          alert('Please select a JPEG or PNG image');
                          return;
                      }
                      
                      // Leer el archivo como Data URL
                      const reader = new FileReader();
                      reader.onload = function(e) {
                          // Comprimir la imagen antes de guardarla
                          const img = new Image();
                          img.onload = function() {
                              // Crear un canvas para comprimir la imagen
                              const canvas = document.createElement('canvas');
                              
                              // Calcular el nuevo tamaño manteniendo la proporción
                              let width = img.width;
                              let height = img.height;
                              const maxSize = 800; // Tamaño máximo para cualquier dimensión
                              
                              if (width > height && width > maxSize) {
                                  height = Math.round(height * (maxSize / width));
                                  width = maxSize;
                              } else if (height > maxSize) {
                                  width = Math.round(width * (maxSize / height));
                                  height = maxSize;
                              }
                              
                              // Establecer el tamaño del canvas
                              canvas.width = width;
                              canvas.height = height;
                              
                              // Dibujar la imagen en el canvas con el nuevo tamaño
                              const ctx = canvas.getContext('2d');
                              ctx.drawImage(img, 0, 0, width, height);
                              
                              // Obtener la imagen comprimida como Data URL (calidad 0.8)
                              const compressedImageData = canvas.toDataURL('image/jpeg', 0.8);
                              
                              // Guardar los datos de la imagen según el índice
                              if (imageIndex === 1) {
                                  image1Data = compressedImageData;
                              } else if (imageIndex === 2) {
                                  image2Data = compressedImageData;
                              } else if (imageIndex === 3) {
                                  image3Data = compressedImageData;
                              }
                              
                              // Mostrar vista previa
                              previewContainer.innerHTML = '';
                              const previewImg = document.createElement('img');
                              previewImg.className = 'max-h-full max-w-full object-contain';
                              previewImg.src = compressedImageData;
                              previewContainer.appendChild(previewImg);
                          };
                          
                          // Cargar la imagen original
                          img.src = e.target.result;
                      };
                      reader.readAsDataURL(file);
                  }
              });
          }
      };
      
      // Configurar los manejadores de eventos para cada imagen
      setupImageUpload(image1Input, selectImage1Btn, image1Preview, 1);
      setupImageUpload(image2Input, selectImage2Btn, image2Preview, 2);
      setupImageUpload(image3Input, selectImage3Btn, image3Preview, 3);
      
      // Manejar el botón de aplicar mosaico
      if (applyMosaicBtn) {
          applyMosaicBtn.addEventListener('click', function() {
              // Obtener el color del marco seleccionado
              let frameColor = 'black'; // Default color
              for (const radio of frameColorRadios) {
                  if (radio.checked) {
                      frameColor = radio.value;
                      break;
                  }
              }
              
              // Obtener el tamaño del marco
              const frameSize = frameSizeSlider.value;
              
              // Crear el objeto de parámetros
              const params = {
                  frame_color: frameColor,
                  frame_size: frameSize
              };
              
              // Añadir las imágenes adicionales si están disponibles
              if (image1Data) {
                  params.image_data_1 = image1Data;
              }
              if (image2Data) {
                  params.image_data_2 = image2Data;
              }
              if (image3Data) {
                  params.image_data_3 = image3Data;
              }
              
              // Aplicar el filtro de mosaico
              applyFilter('4mosaic', params);
          });
      }
  }
  
  // Función para inicializar el control de fusión
  function initializeMergeControl() {
      console.log("Initializing merge control");
      
      const applyMergeBtn = document.getElementById('applyMerge');
      const secondImageInput = document.getElementById('secondImage');
      const selectSecondImageBtn = document.getElementById('selectSecondImageBtn');
      const secondImageName = document.getElementById('secondImageName');
      const secondImagePreview = document.getElementById('secondImagePreview');
      const secondImagePreviewImg = document.getElementById('secondImagePreviewImg');
      const alphaSlider = document.getElementById('alphaSlider');
      const alphaValue = document.getElementById('alphaValue');
      const alphaSliderContainer = document.getElementById('alphaSliderContainer');
      const mergeTypeRadios = document.getElementsByName('mergeType');
      
      // Inicializar variables para la segunda imagen
      let secondImageData = null;
      
      // Manejar la selección del tipo de fusión
      mergeTypeRadios.forEach(radio => {
          radio.addEventListener('change', function() {
              if (this.value === 'alpha') {
                  alphaSliderContainer.classList.remove('hidden');
              } else {
                  alphaSliderContainer.classList.add('hidden');
              }
          });
      });
      
      // Actualizar el valor del slider de alpha
      if (alphaSlider && alphaValue) {
          alphaSlider.addEventListener('input', function() {
              alphaValue.textContent = this.value;
          });
      }
      
      // Manejar el botón de selección de imagen
      if (selectSecondImageBtn && secondImageInput) {
          selectSecondImageBtn.addEventListener('click', function() {
              secondImageInput.click();
          });
      }
      
      // Manejar la selección de archivo
      if (secondImageInput) {
          secondImageInput.addEventListener('change', function() {
              if (this.files && this.files[0]) {
                  const file = this.files[0];
                  
                  // Validar tipo de archivo
                  if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
                      alert('Please select a JPEG or PNG image');
                      return;
                  }
                  
                  // Mostrar nombre del archivo
                  secondImageName.textContent = file.name;
                  
                  // Leer el archivo como Data URL
                  const reader = new FileReader();
                  reader.onload = function(e) {
                      // Comprimir la imagen antes de guardarla
                      const img = new Image();
                      img.onload = function() {
                          // Crear un canvas para comprimir la imagen
                          const canvas = document.createElement('canvas');
                          
                          // Calcular el nuevo tamaño manteniendo la proporción
                          let width = img.width;
                          let height = img.height;
                          const maxSize = 800; // Tamaño máximo para cualquier dimensión
                          
                          if (width > height && width > maxSize) {
                              height = Math.round(height * (maxSize / width));
                              width = maxSize;
                          } else if (height > maxSize) {
                              width = Math.round(width * (maxSize / height));
                              height = maxSize;
                          }
                          
                          // Establecer el tamaño del canvas
                          canvas.width = width;
                          canvas.height = height;
                          
                          // Dibujar la imagen en el canvas con el nuevo tamaño
                          const ctx = canvas.getContext('2d');
                          ctx.drawImage(img, 0, 0, width, height);
                          
                          // Obtener la imagen comprimida como Data URL (calidad 0.8)
                          secondImageData = canvas.toDataURL('image/jpeg', 0.8);
                          
                          // Mostrar vista previa
                          secondImagePreviewImg.src = secondImageData;
                          secondImagePreview.classList.remove('hidden');
                      };
                      
                      // Cargar la imagen original
                      img.src = e.target.result;
                  };
                  reader.readAsDataURL(file);
              }
          });
      }
      
      // Manejar el botón de aplicar fusión
      if (applyMergeBtn) {
          applyMergeBtn.addEventListener('click', function() {
              if (!secondImageData) {
                  alert('Please select a second image to merge');
                  return;
              }
              
              // Obtener el tipo de fusión seleccionado
              let mergeType = 'alpha';
              for (const radio of mergeTypeRadios) {
                  if (radio.checked) {
                      mergeType = radio.value;
                      break;
                  }
              }
              
              // Aplicar el filtro de fusión
              const params = {
                  second_image_data: secondImageData,
                  merge_type: mergeType
              };
              
              // Añadir alpha solo si es necesario
              if (mergeType === 'alpha') {
                  params.alpha = alphaSlider.value;
              }
              
              applyFilter('merge', params);
          });
      }
  }
  
  function addControlEventListeners(filterType) {
      switch (filterType) {
          case 'brightness':
              const brightnessSlider = document.getElementById('brightnessSlider');
              const brightnessValue = document.getElementById('brightnessValue');
              const applyBrightnessBtn = document.getElementById('applyBrightnessBtn');
              
              brightnessSlider.addEventListener('input', function() {
                  brightnessValue.textContent = this.value;
              });
              
              applyBrightnessBtn.addEventListener('click', function() {
                  applyFilter('brightness', { brightness_factor: brightnessSlider.value });
              });
              break;
              
          case 'contrast':
              const contrastSlider = document.getElementById('contrastSlider');
              const contrastValue = document.getElementById('contrastValue');
              const applyContrastBtn = document.getElementById('applyContrastBtn');
              
              contrastSlider.addEventListener('input', function() {
                  contrastValue.textContent = this.value;
              });
              
              applyContrastBtn.addEventListener('click', function() {
                  applyFilter('contrast', { contrast_factor: contrastSlider.value });
              });
              break;
              
          case 'rotate':
              const rotationSlider = document.getElementById('rotationSlider');
              const rotationValue = document.getElementById('rotationValue');
              const applyRotationBtn = document.getElementById('applyRotationBtn');
              
              rotationSlider.addEventListener('input', function() {
                  rotationValue.textContent = `${this.value}°`;
              });
              
              applyRotationBtn.addEventListener('click', function() {
                  applyFilter('rotate', { rotation_angle: rotationSlider.value });
              });
              break;
              
          case 'zoom':
              const zoomSlider = document.getElementById('zoomSlider');
              const zoomValue = document.getElementById('zoomValue');
              const applyZoomBtn = document.getElementById('applyZoomBtn');
              
              zoomSlider.addEventListener('input', function() {
                  zoomValue.textContent = `${this.value}x`;
              });
              
              applyZoomBtn.addEventListener('click', function() {
                  // Use image center for x and y
                  const img = document.getElementById('previewImage');
                  const scale = parseFloat(zoomSlider.value);
                  applyFilter('zoom', { 
                      zoom_scale: scale,
                      zoom_x: img.naturalWidth / 2,
                      zoom_y: img.naturalHeight / 2
                  });
              });
              break;
              
          case 'rgb':
              const applyRGBBtn = document.getElementById('applyRGBBtn');
              
              applyRGBBtn.addEventListener('click', function() {
                  const redChannel = document.getElementById('redChannel').checked;
                  const greenChannel = document.getElementById('greenChannel').checked;
                  const blueChannel = document.getElementById('blueChannel').checked;
                  
                  applyFilter('rgb', { 
                      red: redChannel,
                      green: greenChannel,
                      blue: blueChannel
                  });
              });
              break;
              
          case 'cmy':
              const applyCMYBtn = document.getElementById('applyCMYBtn');
              
              applyCMYBtn.addEventListener('click', function() {
                  const cyanChannel = document.getElementById('cyanChannel').checked;
                  const magentaChannel = document.getElementById('magentaChannel').checked;
                  const yellowChannel = document.getElementById('yellowChannel').checked;
                  
                  applyFilter('cmy', { 
                      cyan: cyanChannel,
                      magenta: magentaChannel,
                      yellow: yellowChannel
                  });
              });
              break;
              
          case 'highlight':
              const applyHighlightBtn = document.getElementById('applyHighlightBtn');
              
              applyHighlightBtn.addEventListener('click', function() {
                  const highlightMode = document.querySelector('input[name="highlightMode"]:checked').value;
                  
                  applyFilter('highlight', { 
                      highlight_mode: highlightMode
                  });
              });
              break;
              
          case 'negative':
              const applyNegativeBtn = document.getElementById('applyNegativeBtn');
              
              applyNegativeBtn.addEventListener('click', function() {
                  applyFilter('negative', {});
              });
              break;
              
          case 'binary':
              const thresholdSlider = document.getElementById('thresholdSlider');
              const thresholdValue = document.getElementById('thresholdValue');
              const applyBinaryBtn = document.getElementById('applyBinaryBtn');
              
              thresholdSlider.addEventListener('input', function() {
                  thresholdValue.textContent = this.value;
              });
              
              applyBinaryBtn.addEventListener('click', function() {
                  applyFilter('binary', { threshold: thresholdSlider.value });
              });
              break;
              
          case 'merge':
              const applyMergeBtn = document.getElementById('applyMergeBtn');
              const secondImageInput = document.getElementById('secondImage');
              const selectSecondImageBtn = document.getElementById('selectSecondImageBtn');
              const secondImageName = document.getElementById('secondImageName');
              const secondImagePreview = document.getElementById('secondImagePreview');
              const secondImagePreviewImg = document.getElementById('secondImagePreviewImg');
              const alphaSlider = document.getElementById('alphaSlider');
              const alphaValue = document.getElementById('alphaValue');
              const alphaSliderContainer = document.getElementById('alphaSliderContainer');
              const mergeTypeRadios = document.getElementsByName('mergeType');
              
              // Inicializar variables para la segunda imagen
              let secondImageData = null;
              
              // Manejar la selección del tipo de fusión
              mergeTypeRadios.forEach(radio => {
                  radio.addEventListener('change', function() {
                      if (this.value === 'alpha') {
                          alphaSliderContainer.classList.remove('hidden');
                      } else {
                          alphaSliderContainer.classList.add('hidden');
                      }
                  });
              });
              
              // Actualizar el valor del slider de alpha
              if (alphaSlider && alphaValue) {
                  alphaSlider.addEventListener('input', function() {
                      alphaValue.textContent = this.value;
                  });
              }
              
              // Manejar el botón de selección de imagen
              if (selectSecondImageBtn && secondImageInput) {
                  selectSecondImageBtn.addEventListener('click', function() {
                      secondImageInput.click();
                  });
              }
              
              // Manejar la selección de archivo
              if (secondImageInput) {
                  secondImageInput.addEventListener('change', function() {
                      if (this.files && this.files[0]) {
                          const file = this.files[0];
                          
                          // Validar tipo de archivo
                          if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
                              alert('Please select a JPEG or PNG image');
                              return;
                          }
                          
                          // Mostrar nombre del archivo
                          secondImageName.textContent = file.name;
                          
                          // Leer el archivo como Data URL
                          const reader = new FileReader();
                          reader.onload = function(e) {
                              // Comprimir la imagen antes de guardarla
                              const img = new Image();
                              img.onload = function() {
                                  // Crear un canvas para comprimir la imagen
                                  const canvas = document.createElement('canvas');
                                  
                                  // Calcular el nuevo tamaño manteniendo la proporción
                                  let width = img.width;
                                  let height = img.height;
                                  const maxSize = 1200; // Tamaño máximo para cualquier dimensión
                                  
                                  if (width > height && width > maxSize) {
                                      height = Math.round(height * (maxSize / width));
                                      width = maxSize;
                                  } else if (height > maxSize) {
                                      width = Math.round(width * (maxSize / height));
                                      height = maxSize;
                                  }
                                  
                                  // Establecer el tamaño del canvas
                                  canvas.width = width;
                                  canvas.height = height;
                                  
                                  // Dibujar la imagen en el canvas con el nuevo tamaño
                                  const ctx = canvas.getContext('2d');
                                  ctx.drawImage(img, 0, 0, width, height);
                                  
                                  // Obtener la imagen comprimida como Data URL (calidad 0.8)
                                  secondImageData = canvas.toDataURL('image/jpeg', 0.8);
                                  
                                  // Mostrar vista previa
                                  secondImagePreviewImg.src = secondImageData;
                                  secondImagePreview.classList.remove('hidden');
                              };
                              
                              // Cargar la imagen original
                              img.src = e.target.result;
                          };
                          reader.readAsDataURL(file);
                      }
                  });
              }
              
              // Manejar el botón de aplicar fusión
              if (applyMergeBtn) {
                  applyMergeBtn.addEventListener('click', function() {
                      if (!secondImageData) {
                          alert('Please select a second image to merge');
                          return;
                      }
                      
                      // Obtener el tipo de fusión seleccionado
                      let mergeType = 'alpha';
                      for (const radio of mergeTypeRadios) {
                          if (radio.checked) {
                              mergeType = radio.value;
                              break;
                          }
                      }
                      
                      // Aplicar el filtro de fusión
                      const params = {
                          second_image_data: secondImageData,
                          merge_type: mergeType
                      };
                      
                      // Añadir alpha solo si es necesario
                      if (mergeType === 'alpha') {
                          params.alpha = alphaSlider.value;
                      }
                      
                      applyFilter('merge', params);
                  });
              }
              break;
      }
  }
  
  function applyFilter(filterType, params) {
      // Show loading spinner
      showLoading(true);
      
      // Comprimir la imagen actual si es necesario
      const compressImage = (dataUrl) => {
          return new Promise((resolve, reject) => {
              const img = new Image();
              img.onload = function() {
                  // Si la imagen es pequeña, no la comprimimos
                  if (img.width <= 1200 && img.height <= 1200) {
                      resolve(dataUrl);
                      return;
                  }
                  
                  // Crear un canvas para comprimir la imagen
                  const canvas = document.createElement('canvas');
                  
                  // Calcular el nuevo tamaño manteniendo la proporción
                  let width = img.width;
                  let height = img.height;
                  const maxSize = 1200; // Tamaño máximo para cualquier dimensión
                  
                  if (width > height && width > maxSize) {
                      height = Math.round(height * (maxSize / width));
                      width = maxSize;
                  } else if (height > maxSize) {
                      width = Math.round(width * (maxSize / height));
                      height = maxSize;
                  }
                  
                  // Establecer el tamaño del canvas
                  canvas.width = width;
                  canvas.height = height;
                  
                  // Dibujar la imagen en el canvas con el nuevo tamaño
                  const ctx = canvas.getContext('2d');
                  ctx.drawImage(img, 0, 0, width, height);
                  
                  // Obtener la imagen comprimida como Data URL (calidad 0.85)
                  resolve(canvas.toDataURL('image/jpeg', 0.85));
              };
              
              img.onerror = function() {
                  reject(new Error('Error al cargar la imagen para compresión'));
              };
              
              img.src = dataUrl;
          });
      };
      
      // Comprimir la imagen actual antes de enviarla
      compressImage(currentImageData)
          .then(compressedImageData => {
              // Create form data
              const formData = new FormData();
              formData.append('image_data', compressedImageData);
              formData.append('filter_type', filterType);
              
              // Add parameters to form data
              for (const key in params) {
                  formData.append(key, params[key]);
              }
              
              // Call API to process image
              return fetch('/process-image/', {
                  method: 'POST',
                  body: formData
              });
          })
          .then(response => response.json())
          .then(data => {
              if (data.error) {
                  console.error('Error:', data.error);
                  alert('Error processing image: ' + data.error);
                  showLoading(false);
                  return;
              }
              
              // Update current image data and preview
              currentImageData = data.processed_image;
              previewImage.src = data.processed_image;
              
              // Generate new histogram
              generateHistogram(data.processed_image)
                  .then(() => {
                      console.log("Histogram updated after filter");
                      showLoading(false);
                  })
                  .catch(error => {
                      console.error("Error updating histogram:", error);
                      showLoading(false);
                  });
          })
          .catch(error => {
              console.error('Error:', error);
              alert('Error processing image: ' + error);
              showLoading(false);
          });
  }
  
  function generateHistogram(imageData) {
      // Devolver una promesa para poder encadenar con .then()
      return new Promise((resolve, reject) => {
          // Verificar que el canvas del histograma exista
          if (!histogramCanvas) {
              console.error('Histogram canvas not found');
              reject(new Error('Histogram canvas not found'));
              return;
          }
          
          // Create form data for histogram generation
          const formData = new FormData();
          formData.append('image_data', imageData);
          
          // Call API to generate histogram
          fetch('/generate-histogram/', {
              method: 'POST',
              body: formData
          })
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
              if (data.error) {
                  console.error('Error:', data.error);
                  reject(new Error(data.error));
                  return;
              }
              
              try {
                  // Display the histogram image
                  const ctx = histogramCanvas.getContext('2d');
                  
                  // Destroy existing chart if it exists
                  if (histogramChart) {
                      histogramChart.destroy();
                  }
                  
                  // Create new chart
                  histogramChart = new Chart(ctx, {
                      type: 'line',
                      data: {
                          labels: Array.from({ length: 256 }, (_, i) => i),
                          datasets: [
                              {
                                  label: 'Luminance',
                                  data: data.histogram_data.luminance,
                                  borderColor: 'white',
                                  borderWidth: 1,
                                  pointRadius: 0,
                                  fill: false
                              },
                              {
                                  label: 'Red',
                                  data: data.histogram_data.red,
                                  borderColor: 'rgba(255, 99, 132, 1)',
                                  borderWidth: 1,
                                  pointRadius: 0,
                                  fill: false
                              },
                              {
                                  label: 'Green',
                                  data: data.histogram_data.green,
                                  borderColor: 'rgba(75, 192, 192, 1)',
                                  borderWidth: 1,
                                  pointRadius: 0,
                                  fill: false
                              },
                              {
                                  label: 'Blue',
                                  data: data.histogram_data.blue,
                                  borderColor: 'rgba(54, 162, 235, 1)',
                                  borderWidth: 1,
                                  pointRadius: 0,
                                  fill: false
                              }
                          ]
                      },
                      options: {
                          responsive: true,
                          maintainAspectRatio: false,
                          scales: {
                              x: {
                                  display: false
                              },
                              y: {
                                  display: false
                              }
                          },
                          plugins: {
                              legend: {
                                  display: false
                              }
                          }
                      }
                  });
                  
                  // Resolver la promesa cuando el histograma se ha generado
                  resolve();
              } catch (error) {
                  console.error('Error creating histogram chart:', error);
                  reject(error);
              }
          })
          .catch(error => {
              console.error('Error generating histogram:', error);
              reject(error);
          });
      });
  }
  
  function resetToOriginalImage() {
      // Reset to original image
      previewImage.src = originalImageData;
      currentImageData = originalImageData;
      
      // Generate histogram for original image
      generateHistogram(originalImageData)
          .then(() => console.log("Histogram reset to original image"))
          .catch(error => console.error("Error resetting histogram:", error));
      
      // Remove active class from all filter options
      filterOptions.forEach(opt => opt.classList.remove('active'));
      
      // Remove filter controls
      const existingControls = document.getElementById('filterControls');
      if (existingControls) {
          existingControls.remove();
      }
  }
  
  function showLoading(show) {
      // Create loading spinner if it doesn't exist
      let spinner = document.getElementById('loadingSpinner');
      if (!spinner) {
          spinner = document.createElement('div');
          spinner.id = 'loadingSpinner';
          spinner.className = 'loading-spinner';
          const container = document.querySelector('.relative.h-96');
          if (container) {
              container.appendChild(spinner);
          }
      }
      
      // Show or hide the spinner
      if (spinner) {
          spinner.style.display = show ? 'block' : 'none';
      }
      
      // Dim the image while loading
      if (previewImage) {
          previewImage.style.opacity = show ? '0.5' : '1';
      }
  }
  
  function resetToOriginalImage() {
      if (originalImageData) {
          currentImageData = originalImageData;
          previewImage.src = originalImageData;
          generateHistogram(originalImageData);
      }
  }
  
  function downloadProcessedImage() {
      if (currentImageData) {
          // Create a temporary link element
          const link = document.createElement('a');
          link.href = currentImageData;
          link.download = 'processed_image.png';
          
          // Append to the document, click it, and remove it
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
      } else {
          alert('No image to download');
      }
  }
});