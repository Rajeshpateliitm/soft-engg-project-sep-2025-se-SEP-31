<template>
  <div class="reset-password-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white text-center py-3">
              <h2 class="mb-0">Reset Password</h2>
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
                    placeholder="Enter your registered email"
                  >
                  <div class="invalid-feedback">
                    Please enter a valid email address.
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="password" class="form-label">New Password</label>
                    <input 
                      type="password" 
                      class="form-control" 
                      id="password" 
                      v-model="formData.password" 
                      required
                      minlength="8"
                      placeholder="At least 8 characters"
                    >
                    <div class="invalid-feedback">
                      Password must be at least 8 characters long.
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="confirmPassword" class="form-label">Confirm Password</label>
                    <input 
                      type="password" 
                      class="form-control" 
                      id="confirmPassword" 
                      v-model="formData.confirmPassword" 
                      required
                      placeholder="Re-enter password"
                    >
                    <div class="invalid-feedback">
                      Passwords must match.
                    </div>
                  </div>
                </div>

                <div v-if="errorMessage" class="alert alert-danger mb-3" role="alert">
                  {{ errorMessage }}
                </div>

                <div v-if="successMessage" class="alert alert-success mb-3" role="alert">
                  {{ successMessage }}
                </div>

                <div class="d-grid gap-2">
                  <button 
                    type="submit" 
                    class="btn btn-primary btn-lg"
                    :disabled="isLoading"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ isLoading ? 'Resetting Password...' : 'Reset Password' }}
                  </button>
                </div>
              </form>

              <div class="text-center mt-4">
                <p class="mb-0">
                  Remember your password? 
                  <router-link to="/signin">Sign in here</router-link>
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
import api from '../services/api';

const router = useRouter();

const formData = ref({
  email: '',
  password: '',
  confirmPassword: ''
});

const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const handleSubmit = async (event) => {
  const form = document.querySelector('.needs-validation');
  errorMessage.value = '';
  successMessage.value = '';
  
  if (form.checkValidity() === false) {
    event.preventDefault();
    event.stopPropagation();
    form.classList.add('was-validated');
    return;
  }

  // Validate password match
  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = 'Passwords do not match';
    form.classList.add('was-validated');
    return;
  }

  // Validate password length
  if (formData.value.password.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters long';
    form.classList.add('was-validated');
    return;
  }

  isLoading.value = true;

  try {
    const response = await api.post('/auth/reset-password', {
      email: formData.value.email,
      new_password: formData.value.password,
      confirm_password: formData.value.confirmPassword
    });

    if (response.status === 200) {
      successMessage.value = 'Password has been successfully reset! Redirecting to sign in...';
      
      // Reset form
      formData.value = {
        email: '',
        password: '',
        confirmPassword: ''
      };
      form.classList.remove('was-validated');

      // Redirect to signin after 2 seconds
      setTimeout(() => {
        router.push('/signin');
      }, 2000);
    }
  } catch (error) {
    console.error('Password reset error:', error);
    if (error.response?.data?.error) {
      errorMessage.value = error.response.data.error;
    } else if (error.response?.data?.message) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value = 'An error occurred while resetting your password. Please try again.';
    }
    form.classList.add('was-validated');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.reset-password-page {
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

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
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

.alert {
  border-radius: 0.375rem;
  border: none;
}

.alert-success {
  background-color: #d1e7dd;
  color: #0f5132;
}

.alert-danger {
  background-color: #f8d7da;
  color: #842029;
}
</style>
