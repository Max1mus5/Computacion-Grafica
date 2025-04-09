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
          generateHistogram(imageData);
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
      // Remove any existing filter control elements
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
      }
  }
  
  function applyFilter(filterType, params) {
      // Show loading spinner
      showLoading(true);
      
      // Create form data
      const formData = new FormData();
      formData.append('image_data', currentImageData);
      formData.append('filter_type', filterType);
      
      // Add parameters to form data
      for (const key in params) {
          formData.append(key, params[key]);
      }
      
      // Call API to process image
      fetch('/process-image/', {
          method: 'POST',
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          if (data.error) {
              console.error('Error:', data.error);
              alert('Error processing image: ' + data.error);
              return;
          }
          
          // Update current image data and preview
          currentImageData = data.processed_image;
          previewImage.src = data.processed_image;
          
          // Generate new histogram
          generateHistogram(data.processed_image);
          
          showLoading(false);
      })
      .catch(error => {
          console.error('Error:', error);
          alert('Error processing image: ' + error);
          showLoading(false);
      });
  }
  
  function generateHistogram(imageData) {
      // Create form data for histogram generation
      const formData = new FormData();
      formData.append('image_data', imageData);
      
      // Call API to generate histogram
      fetch('/generate-histogram/', {
          method: 'POST',
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          if (data.error) {
              console.error('Error:', data.error);
              return;
          }
          
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
      })
      .catch(error => {
          console.error('Error:', error);
      });
  }
  
  function resetToOriginalImage() {
      // Reset to original image
      previewImage.src = originalImageData;
      currentImageData = originalImageData;
      
      // Generate histogram for original image
      generateHistogram(originalImageData);
      
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