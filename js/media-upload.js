document.addEventListener('DOMContentLoaded', function() {
  const dropzone = document.getElementById('mediaDropzone');
  const mediaInput = document.getElementById('media');
  const mediaPreview = document.getElementById('mediaPreview');

  // Previne o comportamento padrão de arrastar e soltar
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Adiciona feedback visual durante o arrasto
  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, unhighlight, false);
  });

  function highlight() {
    dropzone.classList.add('dragover');
  }

  function unhighlight() {
    dropzone.classList.remove('dragover');
  }

  // Manipula o evento de soltar arquivos
  dropzone.addEventListener('drop', handleDrop, false);

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  // Manipula a seleção de arquivos pelo input
  mediaInput.addEventListener('change', function() {
    handleFiles(this.files);
  });

  function handleFiles(files) {
    [...files].forEach(previewFile);
  }

  function previewFile(file) {
    if (!file.type.startsWith('image/') && !file.type.startsWith('video/')) return;

    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onloadend = function() {
      const mediaElement = file.type.startsWith('image/') 
        ? createImagePreview(reader.result)
        : createVideoPreview(reader.result);
      mediaPreview.appendChild(mediaElement);
    };
  }

  function createImagePreview(src) {
    const container = document.createElement('div');
    container.className = 'media-preview-item';
    
    const img = document.createElement('img');
    img.src = src;
    
    const removeButton = createRemoveButton();
    
    container.appendChild(img);
    container.appendChild(removeButton);
    return container;
  }

  function createVideoPreview(src) {
    const container = document.createElement('div');
    container.className = 'media-preview-item';
    
    const video = document.createElement('video');
    video.src = src;
    video.controls = true;
    
    const removeButton = createRemoveButton();
    
    container.appendChild(video);
    container.appendChild(removeButton);
    return container;
  }

  function createRemoveButton() {
    const button = document.createElement('button');
    button.className = 'media-remove-button';
    button.innerHTML = '×';
    button.title = 'Remover mídia';
    
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const mediaItem = this.parentElement;
      mediaItem.remove();
    });
    
    return button;
  }
});