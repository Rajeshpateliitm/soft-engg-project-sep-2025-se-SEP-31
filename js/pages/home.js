const Home = {
    template: `
        <div class="container-fluid vh-100 d-flex align-items-center" style="background-color: #000;">
            <div class="row w-100">
                <!-- Left Side - Image and Message -->
                <div class="col-md-6 d-flex flex-column justify-content-center align-items-center text-white p-5">
                    <div class="text-center">
                        <img src="https://images.unsplash.com/photo-1563453392212-326f5e854473?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80" 
                             alt="Waste Management" 
                             class="img-fluid rounded mb-4"
                             style="max-height: 400px; object-fit: cover;">
                        <h2 class="display-6 fw-bold text-success">For a greener tomorrow</h2>
                    </div>
                </div>
                
                <!-- Right Side - Login Form -->
                <div class="col-md-6 d-flex justify-content-center align-items-center p-5">
                    <div class="card shadow-lg" style="width: 100%; max-width: 400px; background: rgba(255,255,255,0.95);">
                        <div class="card-body p-4">
                            <h3 class="card-title text-center text-dark mb-4">Welcome to WasteWise</h3>
                            
                            <!-- Registration Success Alert -->
                            <div v-if="showRegistrationSuccess" class="alert alert-success mb-3" role="alert">
                                Registration successful! Please login with your credentials.
                            </div>
                            
                            <form @submit.prevent="handleLogin">
                                <!-- Email Input -->
                                <div class="mb-3">
                                    <label for="email" class="form-label text-dark">EMAIL</label>
                                    <input 
                                        type="text" 
                                        class="form-control" 
                                        id="email"
                                        v-model="loginData.email"
                                        placeholder="Enter your email"
                                        maxlength="25"
                                        required
                                        pattern="[a-zA-Z0-9@._-]+"
                                        title="Alphanumeric characters with @ . _ - only">
                                </div>
                                
                                <!-- Password Input -->
                                <div class="mb-3">
                                    <label for="password" class="form-label text-dark">PASSWORD</label>
                                    <input 
                                        type="password" 
                                        class="form-control" 
                                        id="password"
                                        v-model="loginData.password"
                                        placeholder="Enter your password"
                                        maxlength="25"
                                        required
                                        pattern="[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\\|,.<>\/?]+"
                                        title="Alphanumeric and special characters only">
                                </div>
                                
                                <!-- User Type Dropdown -->
                                <div class="mb-4">
                                    <label for="userType" class="form-label text-dark">USER TYPE</label>
                                    <select 
                                        class="form-select" 
                                        id="userType"
                                        v-model="loginData.userType"
                                        required>
                                        <option value="" disabled selected>Select user type</option>
                                        <option value="primary">PRIMARY USER</option>
                                        <option value="secondary">SECONDARY USER</option>
                                        <option value="tertiary">TERTIARY USER</option>
                                    </select>
                                </div>
                                
                                <!-- Login Button -->
                                <div class="d-grid mb-3">
                                    <button type="submit" class="btn btn-success btn-lg">
                                        LOGIN
                                    </button>
                                </div>
                                
                                <!-- Register Button -->
                                <div class="d-grid">
                                    <router-link to="/register" class="btn btn-outline-primary btn-lg">
                                        REGISTER
                                    </router-link>
                                </div>
                            </form>
                            
                            <!-- Login Error Alert Message -->
                            <div v-if="showAlert" class="alert alert-danger mt-3" role="alert">
                                {{ alertMessage }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            loginData: {
                email: '',
                password: '',
                userType: ''
            },
            showAlert: false,
            showRegistrationSuccess: false,
            alertMessage: ''
        };
    },
    mounted() {
        // Check if user came from successful registration
        if (this.$route.query.registered === 'true') {
            this.showRegistrationSuccess = true;
            setTimeout(() => {
                this.showRegistrationSuccess = false;
            }, 5000);
        }
    },
    methods: {
        handleLogin() {
            // Basic validation
            if (!this.loginData.email || !this.loginData.password || !this.loginData.userType) {
                this.showAlertMessage('Please fill in all fields');
                return;
            }
            
            // Email validation (basic alphanumeric with special characters)
            const emailRegex = /^[a-zA-Z0-9@._-]+$/;
            if (!emailRegex.test(this.loginData.email)) {
                this.showAlertMessage('Invalid email format');
                return;
            }
            
            // Password validation (alphanumeric with special characters)
            const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\\|,.<>\/?]+$/;
            if (!passwordRegex.test(this.loginData.password)) {
                this.showAlertMessage('Invalid password format');
                return;
            }
            
            // Length validation
            if (this.loginData.email.length > 25 || this.loginData.password.length > 25) {
                this.showAlertMessage('Email and password must be 25 characters or less');
                return;
            }
            
            // Successful login - redirect based on user type
            this.showAlert = false;
            
            switch(this.loginData.userType) {
                case 'primary':
                    this.$router.push('/primary-dashboard');
                    break;
                case 'secondary':
                    this.$router.push('/secondary-dashboard');
                    break;
                case 'tertiary':
                    this.$router.push('/tertiary-dashboard');
                    break;
                default:
                    this.showAlertMessage('Invalid user type selected');
            }
        },
        
        showAlertMessage(message) {
            this.alertMessage = message;
            this.showAlert = true;
            setTimeout(() => {
                this.showAlert = false;
            }, 3000);
        }
    }
};

export default Home;