
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
        
        coursePreviewModal.addEventListener('hide.bs.modal', function(e){
            console.log(this.querySelector("#video-modal iframe").attr())
            this.querySelector("#video-modal iframe").attr("src", this.querySelector("#video-modal iframe").attr("src"));
            
        })
    }

}

coursePreviewVideo()

// ----------- Header menu

function headerMenu(){
    const menu = document.querySelector('.js-header-menu')
    const backdrop = document.querySelector('.js-header-backdrop')
    const menuCollapseBreakpoint = 911

    function toggleMenu(){
        menu.classList.toggle('open')
        backdrop.classList.toggle('active')
        document.body.classList.toggle('overflow-hidden')
    }

    document.querySelectorAll('.js-header-menu-toggler').forEach((item)=> {
        item.addEventListener('click', toggleMenu)
    })

    // close the menu by cliking outside of it
    backdrop.addEventListener('click', toggleMenu)
    
    function collapse(){
        menu.querySelector('.active .js-sub-menu').removeAttribute('style')
        menu.querySelector('.active').classList.remove('active')
    }

    menu.addEventListener('click', (e) => {
        const { target } = e
        if (target.classList.contains('js-toggle-sub-menu') && window.innerWidth <= menuCollapseBreakpoint) {
            e.preventDefault()

            if (target.parentElement.classList.contains('active')) {
                collapse()
                return
            }

            if (menu.querySelector('.active')) {
                collapse()
            }

            target.parentElement.classList.add('active')
            target.nextElementSibling.style.maxHeight = target.nextElementSibling.scrollHeight + "px"
            
        }
    })

    // when resizing window (useless)
    window.addEventListener('resize', function (){
        if (this.innerWidth > menuCollapseBreakpoint && menu.classList.contains('open')) {
            toggleMenu()
        }

        if (this.innerWidth > menuCollapseBreakpoint && menu.querySelector('.active')) {
            collapse()
        }
    })
}

headerMenu()