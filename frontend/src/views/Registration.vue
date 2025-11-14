<template>
  <div class="registration-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white text-center py-3">
              <h2 class="mb-0">Create Your Account</h2>
            </div>
            <div class="card-body p-4">
              <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
                <div class="mb-3">
                  <label for="fullName" class="form-label">Full Name</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="fullName" 
                    v-model="formData.fullName" 
                    required
                  >
                  <div class="invalid-feedback">
                    Please enter your full name.
                  </div>
                </div>

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

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input 
                      type="password" 
                      class="form-control" 
                      id="password" 
                      v-model="formData.password" 
                      required
                      minlength="8"
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
                    >
                    <div class="invalid-feedback">
                      Passwords must match.
                    </div>
                  </div>
                </div>

                <!-- Note: Only Primary Users (Individuals) can register through public sign-up -->
                <!-- Secondary and Tertiary users are provisioned by administrators -->

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="houseNumber" class="form-label">House Number</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="houseNumber" 
                      v-model="formData.house_number" 
                      required
                    >
                    <div class="invalid-feedback">
                      Please enter your house number.
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="wardNumber" class="form-label">Ward Number</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="wardNumber" 
                      v-model="formData.ward_number" 
                      required
                    >
                    <div class="invalid-feedback">
                      Please enter your ward number.
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="familyMembers" class="form-label">Family Members</label>
                    <input 
                      type="number" 
                      class="form-control" 
                      id="familyMembers" 
                      v-model="formData.family_members" 
                      required
                      min="1"
                    >
                    <div class="invalid-feedback">
                      Please enter number of family members.
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="pincode" class="form-label">Pincode</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="pincode" 
                      v-model="formData.pincode" 
                      required
                      pattern="[0-9]{6}"
                    >
                    <div class="invalid-feedback">
                      Please enter a valid 6-digit pincode.
                    </div>
                  </div>
                </div>

                <div v-if="errorMessage" class="alert alert-danger" role="alert">
                  {{ errorMessage }}
                </div>

                <div class="form-check mb-4">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="terms" 
                    v-model="formData.agreeTerms"
                    required
                  >
                  <label class="form-check-label" for="terms">
                    I agree to the <a href="#" @click.prevent>Terms and Conditions</a>
                  </label>
                  <div class="invalid-feedback">
                    You must agree to the terms and conditions.
                  </div>
                </div>

                <div class="d-grid gap-2">
                  <button 
                    type="submit" 
                    class="btn btn-primary btn-lg"
                    :disabled="isLoading"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ isLoading ? 'Creating Account...' : 'Create Account' }}
                  </button>
                </div>
              </form>

              <div class="text-center mt-4">
                <p class="mb-0">
                  Already have an account? 
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
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const formData = ref({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
  house_number: '',
  ward_number: '',
  family_members: 1,
  pincode: '',
  agreeTerms: false
});

const isLoading = ref(false);
const errorMessage = ref('');

const handleSubmit = async (event) => {
  const form = document.querySelector('.needs-validation');
  errorMessage.value = '';
  
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

  isLoading.value = true;

  try {
    const result = await authStore.register(formData.value);


    if (result.success) {
  // After registration, go to login page
  router.push("/Signin");
}  else {
      errorMessage.value = result.error || 'Registration failed. Please try again.';
    }
  } catch (error) {
    console.error('Registration error:', error);
    errorMessage.value = 'An error occurred during registration. Please try again.';
  } finally {
    isLoading.value = false;
    form.classList.add('was-validated');
  }
};
</script>

<style scoped>
.registration-page {
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
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.invalid-feedback {
  display: none;
  font-size: 0.875rem;
  color: #dc3545;
}

.was-validated .form-control:invalid ~ .invalid-feedback,
.was-validated .form-select:invalid ~ .invalid-feedback,
.was-validated .form-check-input:invalid ~ .invalid-feedback {
  display: block;
}

.was-validated .form-control:invalid,
.was-validated .form-select:invalid,
.was-validated .form-check-input:invalid {
  border-color: #dc3545;
}

a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: #764ba2;
  text-decoration: underline;
}
</style>
