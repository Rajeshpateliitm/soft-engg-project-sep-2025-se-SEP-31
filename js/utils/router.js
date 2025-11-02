// Import all Vue components from the pages folder
import Home from '../pages/home.js';
import Registration from '../pages/registration.js';
import PrimaryUserNavbar from '../pages/primary_user_navbar.js';
import PrimaryUserDashboard from '../pages/primary_user_dashboard.js';
import PrimaryUserQuiz from '../pages/primary_user_quiz.js';
import PrimaryUserWastelog from '../pages/primary_user_wastelog.js';
import PrimaryUserCampaigns from '../pages/primary_user_campaigns.js';
import PrimaryUserQuizPerformance from '../pages/primary_user_quiz_performance.js';
import PrimaryUserCommunityLeaderboard from '../pages/primary_user_community_leaderboard.js';
import PrimaryUserMonthlyEngagement from '../pages/primary_user_monthly_engagement.js';
import PrimaryUserWasteSummary from '../pages/primary_user_waste_summary.js';
import SecondaryUserDashboard from '../pages/secondary_user_dashboard.js';
import TertiaryUserDashboard from '../pages/tertiary_user_dashboard.js';

// Define the routes for the application
const routes = [
    { path: '/', component: Home },
    { path: '/register', component: Registration },
    { 
        path: '/primary-dashboard', 
        component: PrimaryUserNavbar,
        children: [
            { path: '', component: PrimaryUserDashboard },
            { path: 'quiz', component: PrimaryUserQuiz },
            { path: 'wastelog', component: PrimaryUserWastelog },
            { path: 'campaigns', component: PrimaryUserCampaigns },
            { path: 'quiz-performance', component: PrimaryUserQuizPerformance },
            { path: 'community-leaderboard', component: PrimaryUserCommunityLeaderboard },
            { path: 'monthly-engagement', component: PrimaryUserMonthlyEngagement },
            { path: 'waste-summary', component: PrimaryUserWasteSummary }
        ]
    },
    { path: '/secondary-dashboard', component: SecondaryUserDashboard },
    { path: '/tertiary-dashboard', component: TertiaryUserDashboard },
];

const router = new VueRouter({
    mode: 'history',
    routes,
});

export default router;