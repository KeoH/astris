from astris import StyleSheet

stylesheet = StyleSheet()

# Utilities to complement Bootstrap defaults for Astris demos.
stylesheet.add_raw(
    """
:focus-visible {
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.theme-shell {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 35%);
}

.theme-brand-mark {
  width: 1.6rem;
  height: 1.6rem;
  border-radius: 0.45rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #0d6efd, #0b5ed7);
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 700;
}

.theme-hero-art {
  border: 1px solid #dee2e6;
  border-radius: 1rem;
  background: radial-gradient(circle at 10% 0, rgba(13, 110, 253, 0.10), rgba(255, 255, 255, 0));
}
"""
)
