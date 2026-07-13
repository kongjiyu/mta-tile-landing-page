(() => {
  document.documentElement.classList.add("motion-ready");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const reduced = reducedMotion.matches;

  const header = document.querySelector(".site-header");
  if (header) {
    let scrollTicking = false;
    const updateHeader = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
      scrollTicking = false;
    };
    updateHeader();
    window.addEventListener("scroll", () => {
      if (!scrollTicking) {
        scrollTicking = true;
        window.requestAnimationFrame(updateHeader);
      }
    }, { passive: true });
  }

  const toggle = document.querySelector(".menu-toggle");
  const mobileNav = document.querySelector(".mobile-nav");
  if (toggle && mobileNav) {
    mobileNav.querySelectorAll("a").forEach((link, index) => {
      link.style.setProperty("--nav-index", String(index));
    });
    const setMenu = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      mobileNav.classList.toggle("is-open", open);
      document.body.classList.toggle("menu-open", open);
      toggle.textContent = open ? "×" : "☰";
    };
    toggle.addEventListener("click", () => setMenu(toggle.getAttribute("aria-expanded") !== "true"));
    mobileNav.addEventListener("click", (event) => {
      if (event.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setMenu(false);
    });
  }

  document.addEventListener("click", (event) => {
    document.querySelectorAll(".nav-products[open]").forEach((menu) => {
      if (!menu.contains(event.target)) menu.removeAttribute("open");
    });
  });

  const zoomableImages = document.querySelectorAll("main .product-visual img, main .bag");
  if (zoomableImages.length) {
    const lightbox = document.createElement("dialog");
    const shell = document.createElement("div");
    const enlargedImage = document.createElement("img");
    const caption = document.createElement("p");
    const closeButton = document.createElement("button");
    let sourceImage = null;
    let closeTimer;

    lightbox.className = "photo-lightbox";
    lightbox.setAttribute("aria-label", "Enlarged image");
    shell.className = "photo-lightbox-shell";
    enlargedImage.className = "photo-lightbox-image";
    caption.className = "photo-lightbox-caption";
    closeButton.className = "photo-lightbox-close";
    closeButton.type = "button";
    closeButton.setAttribute("aria-label", "Close enlarged image");
    closeButton.textContent = "×";
    shell.append(enlargedImage, caption);
    lightbox.append(shell, closeButton);
    document.body.appendChild(lightbox);

    const finishClose = () => {
      if (lightbox.open) lightbox.close();
      document.body.classList.remove("lightbox-open");
      if (sourceImage) sourceImage.focus();
    };

    const closeLightbox = () => {
      window.clearTimeout(closeTimer);
      lightbox.classList.remove("is-visible");
      if (reduced) {
        finishClose();
      } else {
        closeTimer = window.setTimeout(finishClose, 220);
      }
    };

    const openLightbox = (image) => {
      window.clearTimeout(closeTimer);
      sourceImage = image;
      enlargedImage.src = image.currentSrc || image.src;
      enlargedImage.alt = image.alt || "";
      caption.textContent = image.alt || "Image preview";
      if (typeof lightbox.showModal === "function") {
        if (!lightbox.open) lightbox.showModal();
      } else {
        lightbox.setAttribute("open", "");
      }
      document.body.classList.add("lightbox-open");
      window.requestAnimationFrame(() => lightbox.classList.add("is-visible"));
      closeButton.focus();
    };

    zoomableImages.forEach((image) => {
      const label = image.alt ? `View larger: ${image.alt}` : "View larger image";
      image.classList.add("zoomable-image");
      image.tabIndex = 0;
      image.setAttribute("role", "button");
      image.setAttribute("aria-label", label);
      image.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        openLightbox(image);
      });
      image.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          event.stopPropagation();
          openLightbox(image);
        }
      });
    });

    closeButton.addEventListener("click", closeLightbox);
    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) closeLightbox();
    });
    shell.addEventListener("click", (event) => {
      if (event.target === shell) closeLightbox();
    });
    lightbox.addEventListener("cancel", (event) => {
      event.preventDefault();
      closeLightbox();
    });
  }

  document.querySelectorAll(".tech-details details").forEach((detail) => {
    const summary = detail.querySelector(":scope > summary");
    const content = detail.querySelector(":scope > .detail-content");
    if (!summary || !content) return;

    const inner = document.createElement("div");
    inner.className = "detail-content-inner";
    while (content.firstChild) inner.appendChild(content.firstChild);
    content.appendChild(inner);

    const setExpandedState = (expanded) => {
      summary.setAttribute("aria-expanded", String(expanded));
      detail.classList.toggle("is-expanded", expanded);
    };

    setExpandedState(detail.open);
    if (reduced) {
      detail.addEventListener("toggle", () => setExpandedState(detail.open));
      return;
    }

    let transitionTimer;
    let transitionFrame;
    summary.addEventListener("click", (event) => {
      event.preventDefault();
      window.clearTimeout(transitionTimer);
      window.cancelAnimationFrame(transitionFrame);

      const shouldOpen = !detail.classList.contains("is-expanded");
      detail.classList.add("is-animating");
      summary.setAttribute("aria-expanded", String(shouldOpen));

      if (shouldOpen) {
        detail.open = true;
        transitionFrame = window.requestAnimationFrame(() => {
          transitionFrame = window.requestAnimationFrame(() => {
            detail.classList.add("is-expanded");
          });
        });
      } else {
        detail.classList.remove("is-expanded");
      }

      transitionTimer = window.setTimeout(() => {
        detail.classList.remove("is-animating");
        if (!shouldOpen) detail.open = false;
      }, 440);
    });
  });

  const reveals = document.querySelectorAll(".reveal");
  const revealGroups = new WeakMap();
  reveals.forEach((el) => {
    const parent = el.parentElement;
    const index = revealGroups.get(parent) || 0;
    el.style.setProperty("--reveal-delay", `${Math.min(index, 3) * 70}ms`);
    revealGroups.set(parent, index + 1);
  });
  if (reduced || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-visible"));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach((el) => observer.observe(el));
  }
})();
