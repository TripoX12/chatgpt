const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
const floatingCta = document.querySelector('.floating-cta');
const footer = document.querySelector('.site-footer');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (menuToggle && nav) {
  menuToggle.addEventListener('click', () => {
    const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('open');
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('click', (event) => {
    const clickInside = nav.contains(event.target) || menuToggle.contains(event.target);
    if (!clickInside) {
      nav.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      nav.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.focus();
    }
  });
}

if (!prefersReducedMotion && 'IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
        }
      });
    },
    { threshold: 0.14 }
  );

  document.querySelectorAll('.section .container').forEach((block) => {
    block.classList.add('reveal');
    revealObserver.observe(block);
  });
}

if (floatingCta) {
  const onScroll = () => {
    const shouldShow = window.scrollY > 620;
    floatingCta.classList.toggle('visible', shouldShow);

    if (footer) {
      const footerTop = footer.getBoundingClientRect().top;
      const overlapsFooter = footerTop < window.innerHeight - 100;
      floatingCta.style.opacity = overlapsFooter ? '0' : '';
      floatingCta.style.pointerEvents = overlapsFooter ? 'none' : '';
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

const form = document.querySelector('.contact-card');
const feedback = document.querySelector('.form-feedback');

if (form && feedback) {
  const submitButton = form.querySelector('button[type="submit"]');
  const defaultButtonText =
    submitButton?.getAttribute('data-submit-label') || submitButton?.textContent?.trim() || 'Enviar';
  let isSubmitting = false;

  const setFeedback = (message, status) => {
    feedback.textContent = message;
    feedback.classList.remove('success', 'error', 'is-loading');
    if (status) {
      feedback.classList.add(status);
    }
  };

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (isSubmitting || !form.reportValidity()) {
      return;
    }

    isSubmitting = true;
    form.setAttribute('aria-busy', 'true');

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = 'Enviando solicitud...';
    }

    setFeedback('Enviando solicitud...', 'is-loading');

    try {
      const formData = new FormData(form);
      const telefonoRaw = (formData.get('telefono') || '').toString().trim();

      if (telefonoRaw) {
        const normalizedDigits = telefonoRaw.replace(/\D/g, '');
        let normalizedPhone = telefonoRaw;

        if (normalizedDigits.startsWith('34') && normalizedDigits.length === 11) {
          normalizedPhone = `+${normalizedDigits}`;
        } else if (normalizedDigits.length === 9) {
          normalizedPhone = `+34${normalizedDigits}`;
        }

        formData.set('telefono', normalizedPhone);
      }

      const response = await fetch(form.action, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('formspree-request-failed');
      }

      setFeedback(
        'Solicitud enviada correctamente. Revisaré tu mensaje y te responderé lo antes posible.',
        'success'
      );
      form.reset();
    } catch (error) {
      setFeedback('No se pudo enviar la solicitud. Vuelve a intentarlo en unos segundos.', 'error');
    } finally {
      isSubmitting = false;
      form.removeAttribute('aria-busy');
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = defaultButtonText;
      }
    }
  });
}

const yearEl = document.getElementById('year');
if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}
