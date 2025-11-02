const PrimaryUserNavbar = {
    template: `
        <div>
            <!-- Navbar -->
            <nav class="navbar navbar-expand-lg navbar-light fixed-top" 
                 :style="navbarStyle"
                 @mouseenter="navbarHover = true"
                 @mouseleave="navbarHover = false">
                <div class="container-fluid">
                    <!-- Navbar Brand -->
                    <a class="navbar-brand fw-bold text-dark" href="#">WASTEWISE</a>
                    
                    <!-- Navbar Toggler -->
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    
                    <!-- Navbar Items -->
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav me-auto">
                            <li class="nav-item">
                                <router-link to="/primary-dashboard" class="nav-link text-dark fw-semibold">
                                    DASHBOARD
                                </router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/primary-dashboard/quiz" class="nav-link text-dark fw-semibold">
                                    QUIZ
                                </router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/primary-dashboard/wastelog" class="nav-link text-dark fw-semibold">
                                    WASTELOG
                                </router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/primary-dashboard/campaigns" class="nav-link text-dark fw-semibold">
                                    CAMPAIGNS
                                </router-link>
                            </li>
                        </ul>
                        
                        <!-- Right side items -->
                        <ul class="navbar-nav">
                            <li class="nav-item">
                                <span class="nav-link text-dark fw-semibold">
                                    <i class="bi bi-clock"></i> {{ currentDateTime }}
                                </span>
                            </li>
                            <li class="nav-item">
                                <span class="nav-link text-dark fw-semibold">
                                    <i class="bi bi-person"></i> XYZABC
                                </span>
                            </li>
                            <li class="nav-item">
                                <router-link to="/" class="btn btn-outline-danger btn-sm ms-2">
                                    LOGOUT
                                </router-link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            
            <!-- Main Content Area -->
            <div class="container-fluid" style="padding-top: 80px; min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div class="container py-4">
                    <router-view></router-view>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            navbarHover: false,
            currentDateTime: ''
        };
    },
    computed: {
        navbarStyle() {
            const baseStyle = {
                border: '2px solid #000',
                transition: 'background-color 0.3s ease',
                padding: '10px 0'
            };
            
            if (this.navbarHover) {
                return {
                    ...baseStyle,
                    backgroundColor: '#464A9E'
                };
            } else {
                return {
                    ...baseStyle,
                    backgroundColor: 'transparent'
                };
            }
        }
    },
    mounted() {
        this.updateDateTime();
        // Update time every second
        this.interval = setInterval(this.updateDateTime, 1000);
    },
    beforeDestroy() {
        clearInterval(this.interval);
    },
    methods: {
        updateDateTime() {
            this.currentDateTime = new Date().toISOString().replace('T', ' ').substring(0, 19);
        }
    }
};

export default PrimaryUserNavbar;