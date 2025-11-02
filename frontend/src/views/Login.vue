<template>
  <div class="login-container">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-md-4">
        <div class="card shadow">
          <div class="card-body p-4">
            <div class="text-center mb-4">
              <h2>Welcome Back</h2>
              <p class="text-muted">Please sign in to continue</p>
            </div>
            
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="email" 
                  v-model="email" 
                  required
                  placeholder="Enter your email">
              </div>
              
              <div class="mb-3">
                <div class="d-flex justify-content-between">
                  <label for="password" class="form-label">Password</label>
                  <a href="#" class="text-decoration-none small">
                    Forgot password?
                  </a>
                </div>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="password" 
                  required
                  placeholder="Enter your password">
              </div>
              
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">
                  Sign In
                </button>
                
                <div class="text-center my-3">
                  <span class="text-muted">or</span>
                </div>
                
                <button type="button" class="btn btn-outline-secondary" @click="signInWithGoogle">
                  <i class="bi bi-google me-2"></i> Sign in with Google
                </button>
              </div>
              
              <div class="text-center mt-3">
                <p class="mb-0">
                  Don't have an account? 
                  <router-link to="/register" class="text-decoration-none">
                    Sign up
                  </router-link>
                </p>
              </div>
            </form>
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
const email = ref('');
const password = ref('');

const handleLogin = () => {
  console.log('Login attempt with:', email.value);
  // Redirect to dashboard or home page
  router.push('/');
};

const signInWithGoogle = () => {
  console.log('Sign in with Google');
};
</script>

<style scoped>
.login-container {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 20px;
}

.card {
  border: none;
  border-radius: 10px;
  overflow: hidden;
}

.btn-google {
  background-color: #fff;
  color: #757575;
  border: 1px solid #ddd;
}

.btn-google:hover {
  background-color: #f8f9fa;
  border-color: #ccc;
}

.form-control:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Add some nice animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fadeIn 0.3s ease-out;
}
</style>
