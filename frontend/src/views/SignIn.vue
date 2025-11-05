<template>
  <div class="signin-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white text-center py-3">
              <h2 class="mb-0">Sign In</h2>
            </div>
            <div class="card-body p-4">
              <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
                <div class="mb-3">
                  <label for="email" class="form-label">Email Address</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    id="email" 
                    v-model="formData.email" 
                    required
                  >
                  <div class="invalid-feedback">
                    Please enter a valid email address.
                  </div>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="formData.password" 
                    required
                    minlength="6"
                  >
                  <div class="invalid-feedback">
                    Password must be at least 6 characters long.
                  </div>
                </div>

                <div class="mb-3">
                  <label for="userType" class="form-label">I am a</label>
                  <select 
                    class="form-select" 
                    id="userType" 
                    v-model="formData.userType"
                    required
                  >
                    <option value="" disabled>Select user type</option>
                    <option value="primary">Primary User (Individual)</option>
                    <option value="secondary">Secondary User (Organization)</option>
                    <option value="tertiary">Tertiary User (Municipality)</option>
                  </select>
                  <div class="invalid-feedback">
                    Please select a user type.
                  </div>
                </div>

                <div class="d-flex justify-content-between align-items-center mb-4">
                  <div class="form-check">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      id="rememberMe" 
                      v-model="formData.rememberMe"
                    >
                    <label class="form-check-label" for="rememberMe">
                      Remember me
                    </label>
                  </div>
                  <div>
                    <a href="#" class="text-primary">Forgot password?</a>
                  </div>
                </div>

                <div class="d-grid gap-2">
                  <button type="submit" class="btn btn-primary btn-lg">
                    Sign In
                  </button>
                </div>
              </form>

              <div class="text-center mt-4">
                <p class="mb-0">
                  Don't have an account? 
                  <router-link to="/register">Sign up here</router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const formData = ref({
  email: '',
  password: '',
  userType: '',
  rememberMe: false
});

const handleSubmit = () => {
  const form = document.querySelector('.needs-validation');
  
  if (form.checkValidity() === false) {
    event.preventDefault();
    event.stopPropagation();
  } else {
    // TODO: Implement actual authentication
    console.log('Signing in with:', formData.value);
    
    // Redirect based on user type after successful sign in
    switch(formData.value.userType) {
      case 'primary':
        router.push('/primary-dashboard');
        break;
      case 'secondary':
        router.push('/secondary-dashboard');
        break;
      case 'tertiary':
        router.push('/tertiary-dashboard');
        break;
      default:
        router.push('/');
    }
  }
  
  form.classList.add('was-validated');
};
</script>

<style scoped>
.signin-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem 0;
}

.card {
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-bottom: none;
}

.form-control:focus, .form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.25rem rgba(102, 126, 234, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

a {
  text-decoration: none;
  transition: all 0.3s ease;
}

a:hover {
  text-decoration: underline;
}

.invalid-feedback {
  display: none;
  width: 100%;
  margin-top: 0.25rem;
  font-size: 0.875em;
  color: #dc3545;
}

.was-validated .form-control:invalid ~ .invalid-feedback,
.was-validated .form-control:invalid ~ .invalid-tooltip,
.form-control.is-invalid ~ .invalid-feedback,
.form-control.is-invalid ~ .invalid-tooltip {
  display: block;
}

.was-validated .form-control:invalid,
.form-control.is-invalid {
  border-color: #dc3545;
  padding-right: calc(1.5em + 0.75rem);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
}
</style>
