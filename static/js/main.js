

// ------------------- Testimonial Slider 

function testimonialSlider(){
    const carouselOne = document.getElementById('carouselOne')
    if (carouselOne) {
        carouselOne.addEventListener('slide.bs.carousel', function () {
            const activeItem = this.querySelector('.active')
            document.querySelector('.js-testimonial-img').src = activeItem.getAttribute('data-js-testimonial-img')
          })
    } 
}

testimonialSlider()


// ----------- couurse preview

function coursePreviewVideo(){
    const coursePreviewModal = document.querySelector('.js-course-preview-modal')
    if (coursePreviewModal) {
        coursePreviewModal.addEventListener('shown.bs.modal', function (){
            this.querySelector('.js-course-preview-video').play()
            this.querySelector('.js-course-preview-video').currentTime = 0
        })
        
        coursePreviewModal.addEventListener('hide.bs.modal', function(){
            this.querySelector('.js-course-preview-video').pause() 
        })
    }

}

coursePreviewVideo()

// ----------- Header menu

function headerMenu(){
    const menu = document.querySelector('js-header-menu')
    const backdrop = document.querySelector('js-header-backdrop')
    const menuCollapseBreakpoint = 911

    menu.addEventListener('click', (e) => {
        
    })
}

headerMenu()