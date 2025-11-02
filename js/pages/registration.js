const Registration = {
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
                
                <!-- Right Side - Registration Form -->
                <div class="col-md-6 d-flex justify-content-center align-items-center p-5">
                    <div class="card shadow-lg" style="width: 100%; max-width: 450px; background: rgba(255,255,255,0.95);">
                        <div class="card-body p-4">
                            <h3 class="card-title text-center text-dark mb-4">Create Your Account</h3>
                            
                            <form @submit.prevent="handleRegistration">
                                <!-- Email Input -->
                                <div class="mb-3">
                                    <label for="email" class="form-label text-dark">EMAIL</label>
                                    <input 
                                        type="text" 
                                        class="form-control" 
                                        id="email"
                                        v-model="registrationData.email"
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
                                        v-model="registrationData.password"
                                        placeholder="Enter your password"
                                        maxlength="25"
                                        required
                                        pattern="[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\\|,.<>\/?]+"
                                        title="Alphanumeric and special characters only">
                                </div>
                                
                                <!-- House Number Input -->
                                <div class="mb-3">
                                    <label for="houseNumber" class="form-label text-dark">HOUSE NUMBER</label>
                                    <input 
                                        type="text" 
                                        class="form-control" 
                                        id="houseNumber"
                                        v-model="registrationData.houseNumber"
                                        placeholder="Enter house number"
                                        maxlength="25"
                                        required
                                        pattern="[a-zA-Z0-9]+"
                                        title="Alphanumeric characters only">
                                </div>
                                
                                <!-- Ward Number Input -->
                                <div class="mb-3">
                                    <label for="wardNumber" class="form-label text-dark">WARD NUMBER</label>
                                    <input 
                                        type="number" 
                                        class="form-control" 
                                        id="wardNumber"
                                        v-model="registrationData.wardNumber"
                                        placeholder="Enter ward number"
                                        maxlength="10"
                                        required
                                        pattern="[0-9]+"
                                        title="Numeric characters only">
                                </div>
                                
                                <!-- Family Members Input -->
                                <div class="mb-3">
                                    <label for="familyMembers" class="form-label text-dark">FAMILY MEMBERS</label>
                                    <input 
                                        type="number" 
                                        class="form-control" 
                                        id="familyMembers"
                                        v-model="registrationData.familyMembers"
                                        placeholder="Enter number of family members"
                                        maxlength="10"
                                        required
                                        pattern="[0-9]+"
                                        title="Numeric characters only">
                                </div>
                                
                                <!-- Pincode Input -->
                                <div class="mb-3">
                                    <label for="pincode" class="form-label text-dark">PINCODE</label>
                                    <input 
                                        type="number" 
                                        class="form-control" 
                                        id="pincode"
                                        v-model="registrationData.pincode"
                                        placeholder="Enter pincode"
                                        maxlength="10"
                                        required
                                        pattern="[0-9]+"
                                        title="Numeric characters only">
                                </div>
                                
                                <!-- User Category Dropdown -->
                                <div class="mb-4">
                                    <label for="userCategory" class="form-label text-dark">USER CATEGORY</label>
                                    <select 
                                        class="form-select" 
                                        id="userCategory"
                                        v-model="registrationData.userCategory"
                                        required>
                                        <option value="" disabled selected>Select user category</option>
                                        <option value="primary">Primary User</option>
                                        <option value="secondary">Secondary User</option>
                                        <option value="tertiary">Tertiary User</option>
                                    </select>
                                </div>
                                
                                <!-- Register Button -->
                                <div class="d-grid mb-3">
                                    <button type="submit" class="btn btn-success btn-lg">
                                        REGISTER
                                    </button>
                                </div>
                                
                                <!-- Back to Login Button -->
                                <div class="d-grid">
                                    <router-link to="/" class="btn btn-outline-primary btn-lg">
                                        Back to Login
                                    </router-link>
                                </div>
                            </form>
                            
                            <!-- Success Alert Message -->
                            <div v-if="showSuccessAlert" class="alert alert-success mt-3" role="alert">
                                {{ successMessage }}
                            </div>
                            
                            <!-- Error Alert Message -->
                            <div v-if="showErrorAlert" class="alert alert-danger mt-3" role="alert">
                                {{ errorMessage }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            registrationData: {
                email: '',
                password: '',
                houseNumber: '',
                wardNumber: '',
                familyMembers: '',
                pincode: '',
                userCategory: ''
            },
            showSuccessAlert: false,
            showErrorAlert: false,
            successMessage: '',
            errorMessage: ''
        };
    },
    methods: {
        handleRegistration() {
            // Reset alerts
            this.showSuccessAlert = false;
            this.showErrorAlert = false;

            // Check if all fields are filled
            if (!this.registrationData.email || 
                !this.registrationData.password || 
                !this.registrationData.houseNumber || 
                !this.registrationData.wardNumber || 
                !this.registrationData.familyMembers || 
                !this.registrationData.pincode || 
                !this.registrationData.userCategory) {
                this.showErrorMessage('Please fill in all fields');
                return;
            }

            // Email validation
            const emailRegex = /^[a-zA-Z0-9@._-]+$/;
            if (!emailRegex.test(this.registrationData.email)) {
                this.showErrorMessage('Invalid email format. Use only alphanumeric characters and @ . _ -');
                return;
            }

            // Password validation
            const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\\|,.<>\/?]+$/;
            if (!passwordRegex.test(this.registrationData.password)) {
                this.showErrorMessage('Invalid password format. Use alphanumeric and special characters only');
                return;
            }

            // House Number validation
            const houseNumberRegex = /^[a-zA-Z0-9]+$/;
            if (!houseNumberRegex.test(this.registrationData.houseNumber)) {
                this.showErrorMessage('Invalid house number. Use alphanumeric characters only');
                return;
            }

            // Ward Number validation (numeric)
            const wardNumberRegex = /^[0-9]+$/;
            if (!wardNumberRegex.test(this.registrationData.wardNumber.toString())) {
                this.showErrorMessage('Ward number must contain only numbers');
                return;
            }

            // Family Members validation (numeric)
            const familyMembersRegex = /^[0-9]+$/;
            if (!familyMembersRegex.test(this.registrationData.familyMembers.toString())) {
                this.showErrorMessage('Family members must contain only numbers');
                return;
            }

            // Pincode validation (numeric)
            const pincodeRegex = /^[0-9]+$/;
            if (!pincodeRegex.test(this.registrationData.pincode.toString())) {
                this.showErrorMessage('Pincode must contain only numbers');
                return;
            }

            // Length validations
            if (this.registrationData.email.length > 25) {
                this.showErrorMessage('Email must be 25 characters or less');
                return;
            }

            if (this.registrationData.password.length > 25) {
                this.showErrorMessage('Password must be 25 characters or less');
                return;
            }

            if (this.registrationData.houseNumber.length > 25) {
                this.showErrorMessage('House number must be 25 characters or less');
                return;
            }

            if (this.registrationData.wardNumber.toString().length > 10) {
                this.showErrorMessage('Ward number must be 10 digits or less');
                return;
            }

            if (this.registrationData.familyMembers.toString().length > 10) {
                this.showErrorMessage('Family members must be 10 digits or less');
                return;
            }

            if (this.registrationData.pincode.toString().length > 10) {
                this.showErrorMessage('Pincode must be 10 digits or less');
                return;
            }

            // All validations passed - show success message
            this.showSuccessMessage('Registration successful! Redirecting to login...');
            
            // Redirect to home page after 2 seconds
            setTimeout(() => {
                this.$router.push('/');
            }, 2000);
        },
        
        showSuccessMessage(message) {
            this.successMessage = message;
            this.showSuccessAlert = true;
        },
        
        showErrorMessage(message) {
            this.errorMessage = message;
            this.showErrorAlert = true;
            setTimeout(() => {
                this.showErrorAlert = false;
            }, 5000);
        }
    }
};

export default Registration;