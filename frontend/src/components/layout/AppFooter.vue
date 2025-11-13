<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-content">
        <div class="footer-row">
          <!-- About Section -->
          <div class="footer-col">
            <h5 class="footer-title">WASTEWISE</h5>
            <p class="footer-description">
              A comprehensive waste management system promoting sustainable practices and environmental responsibility.
            </p>
          </div>
          
          <!-- Quick Links -->
          <div class="footer-col">
            <h6 class="footer-heading">Quick Links</h6>
            <ul class="footer-links">
              <li><router-link to="/">Home</router-link></li>
              <li><router-link to="/signin">Login</router-link></li>
              <li><router-link to="/register">Register</router-link></li>
            </ul>
          </div>
          
          <!-- Resources -->
          <div class="footer-col">
            <h6 class="footer-heading">Resources</h6>
            <ul class="footer-links">
              <li><a href="#waste-management">Waste Management</a></li>
              <li><a href="#recycling">Recycling Guide</a></li>
              <li><a href="#campaigns">Campaigns</a></li>
            </ul>
          </div>
          
          <!-- Contact -->
          <div class="footer-col">
            <h6 class="footer-heading">Contact</h6>
            <ul class="footer-contact">
              <li>
                <i class="bi bi-envelope me-2"></i>
                <a href="mailto:info@wastewise.com">info@wastewise.com</a>
              </li>
              <li>
                <i class="bi bi-telephone me-2"></i>
                <a href="tel:+1234567890">+1 (234) 567-890</a>
              </li>
            </ul>
          </div>
        </div>
        
        <!-- Copyright -->
        <div class="footer-bottom">
          <p class="copyright-text">
            &copy; {{ currentYear }} WasteWise. All rights reserved.
          </p>
          <div class="footer-legal">
            <a href="#privacy">Privacy</a>
            <span class="separator">|</span>
            <a href="#terms">Terms</a>
            <span class="separator">|</span>
            <a href="#cookies">Cookies</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';

const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>


.app-footer {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: #e0e0e0;
  margin-top: auto;
  padding: 1rem 0; /* ⬅ Reduced height */
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  width: 100vw;
  margin-left: calc(50% - 50vw);
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: auto;
  min-height: fit-content;
}

.footer-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.footer-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 3rem;
  margin-bottom: 0.75rem; /* ⬅ Reduced spacing */
}


.footer-col {
  display: flex;
  flex-direction: column;
}

.footer-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.75rem;
  letter-spacing: 0.5px;
}

.footer-description {
  font-size: 0.85rem;
  line-height: 1.5;
  color: #b0b0b0;
  margin: 0;
}

.footer-heading {
  font-size: 0.9rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.5rem;
}

.footer-links a {
  color: #b0b0b0;
  text-decoration: none;
  font-size: 0.85rem;
  transition: all 0.2s ease;
  display: inline-block;
}

.footer-links a:hover {
  color: #fff;
  transform: translateX(3px);
}

.footer-contact {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-contact li {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  color: #b0b0b0;
  font-size: 0.85rem;
}

.footer-contact i {
  color: #4a9eff;
  font-size: 0.9rem;
}

.footer-contact a {
  color: #b0b0b0;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-contact a:hover {
  color: #fff;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
  gap: 1rem;
}

.copyright-text {
  margin: 0;
  color: #b0b0b0;
  font-size: 0.8rem;
}

.footer-legal {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-legal a {
  color: #b0b0b0;
  text-decoration: none;
  font-size: 0.8rem;
  transition: color 0.2s ease;
}

.footer-legal a:hover {
  color: #fff;
}

.separator {
  color: #666;
}

/* Dark mode adjustments */
.dark-mode .app-footer {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-top-color: rgba(255, 255, 255, 0.05);
}

.dark-mode .footer-title,
.dark-mode .footer-heading {
  color: #fff;
}

.dark-mode .footer-description,
.dark-mode .footer-links a,
.dark-mode .footer-contact {
  color: #c0c0c0;
}

.dark-mode .footer-links a:hover,
.dark-mode .footer-contact a:hover {
  color: #4a9eff;
}

.dark-mode .footer-bottom {
  border-top-color: rgba(255, 255, 255, 0.05);
}

/* Responsive */
@media (max-width: 992px) {
  .footer-row {
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .app-footer {
    padding: 1.5rem 0 0.75rem;
  }
  
  .footer-content {
    padding: 0 1rem;
  }
  
  .footer-row {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .footer-bottom {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .footer-legal {
    justify-content: center;
  }
}
</style>
