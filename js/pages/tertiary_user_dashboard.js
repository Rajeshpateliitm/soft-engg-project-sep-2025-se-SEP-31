const TertiaryUserDashboard = {
    template: `
        <div class="container-fluid" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); min-height: 100vh;">
            <div class="container py-5">
                <div class="row">
                    <div class="col-12">
                        <div class="card shadow-lg">
                            <div class="card-header bg-dark text-white">
                                <div class="d-flex justify-content-between align-items-center">
                                    <h3 class="mb-0">Tertiary User Dashboard</h3>
                                    <router-link to="/" class="btn btn-light btn-sm">
                                        Logout
                                    </router-link>
                                </div>
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-md-4 mb-4">
                                        <div class="card bg-warning text-dark">
                                            <div class="card-body">
                                                <h5>Admin Panel</h5>
                                                <p class="mb-0">System management</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-4">
                                        <div class="card bg-info text-white">
                                            <div class="card-body">
                                                <h5>User Management</h5>
                                                <p class="mb-0">Manage all users</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-4">
                                        <div class="card bg-success text-white">
                                            <div class="card-body">
                                                <h5>System Analytics</h5>
                                                <p class="mb-0">Overall platform stats</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};

export default TertiaryUserDashboard;