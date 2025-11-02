const SecondaryUserDashboard = {
    template: `
        <div class="container-fluid" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
            <div class="container py-5">
                <div class="row">
                    <div class="col-12">
                        <div class="card shadow-lg">
                            <div class="card-header bg-primary text-white">
                                <div class="d-flex justify-content-between align-items-center">
                                    <h3 class="mb-0">Secondary User Dashboard</h3>
                                    <router-link to="/" class="btn btn-light btn-sm">
                                        Logout
                                    </router-link>
                                </div>
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-md-4 mb-4">
                                        <div class="card bg-success text-white">
                                            <div class="card-body">
                                                <h5>Data Analytics</h5>
                                                <p class="mb-0">View waste statistics</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-4">
                                        <div class="card bg-danger text-white">
                                            <div class="card-body">
                                                <h5>Reports</h5>
                                                <p class="mb-0">Generate insights</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-4">
                                        <div class="card bg-secondary text-white">
                                            <div class="card-body">
                                                <h5>Monitoring</h5>
                                                <p class="mb-0">Track community progress</p>
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

export default SecondaryUserDashboard;