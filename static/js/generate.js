var dropArea = document.getElementById('drop-area')

dropArea.addEventListener('dragenter', function (e) {
  e.preventDefault()
  // クラス名を追加
  dropArea.classList.add('active')
  console.log('dragenter')
})

dropArea.addEventListener('dragleave', function (event) {
  insideDragArea = false
  console.log('dragleave')
  if ([...event.target.classList].includes('item')) {
    return
  }
  dropArea.classList.remove('active')
})

dropArea.addEventListener('drop', function (e) {
  e.preventDefault()
  dropArea.classList.remove('active')

  var file = e.dataTransfer.files[0]
  var formData = new FormData()
  formData.append('file', file)

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message)
    })
})