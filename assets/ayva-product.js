(function () {
  function wireGallery(root) {
    var thumbs = root.querySelector('.ayva-gallery__thumbs');
    if (!thumbs) return;

    thumbs.addEventListener('click', function (e) {
      var btn = e.target.closest('.ayva-gallery__thumb');
      if (!btn) return;
      var id = btn.getAttribute('data-thumb-id');
      var activeThumb = root.querySelector('.ayva-gallery__thumb.is-active');
      if (activeThumb) activeThumb.classList.remove('is-active');
      btn.classList.add('is-active');
      var activeSlide = root.querySelector('.ayva-gallery__slide.is-active');
      if (activeSlide) activeSlide.classList.remove('is-active');
      var nextSlide = root.querySelector('.ayva-gallery__slide[data-media-id="' + id + '"]');
      if (nextSlide) nextSlide.classList.add('is-active');
    });
  }

  function wireVariantLabels(root) {
    root.querySelectorAll('.ayva-variants__group').forEach(function (group) {
      group.addEventListener('change', function (e) {
        if (e.target.type !== 'radio') return;
        var label = group.querySelector('[data-selected-value]');
        if (label) label.textContent = e.target.value;
      });
    });
  }

  function init() {
    document.querySelectorAll('.ayva-product').forEach(function (root) {
      wireGallery(root);
      wireVariantLabels(root);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
