import { createRouter, createWebHistory } from 'vue-router';

// Lazy load components for better performance
const Home = () => import('@/views/Home.vue');
const Registration = () => import('@/views/Registration.vue');
const PrimaryUserNavbar = () => import('@/components/layout/PrimaryUserNavbar.vue');
const PrimaryUserDashboard = () => import('@/views/primary/PrimaryUserDashboard.vue');
const PrimaryUserQuiz = () => import('@/views/primary/PrimaryUserQuiz.vue');
const PrimaryUserWastelog = () => import('@/views/primary/PrimaryUserWastelog.vue');
const PrimaryUserCampaigns = () => import('@/views/primary/PrimaryUserCampaigns.vue');
const PrimaryUserQuizPerformance = () => import('@/views/primary/PrimaryUserQuizPerformance.vue');
const PrimaryUserCommunityLeaderboard = () => import('@/views/primary/PrimaryUserCommunityLeaderboard.vue');
const PrimaryUserMonthlyEngagement = () => import('@/views/primary/PrimaryUserMonthlyEngagement.vue');
const PrimaryUserWasteSummary = () => import('@/views/primary/PrimaryUserWasteSummary.vue');
const SecondaryUserDashboard = () => import('@/views/SecondaryUserDashboard.vue');
const TertiaryUserDashboard = () => import('@/views/TertiaryUserDashboard.vue');
const RWANavbar = () => import('@/components/layout/RWANavbar.vue');
const RWADashboard = () => import('@/views/rwa/RWADashboard.vue');
const RWALeaderboard = () => import('@/views/rwa/RWALeaderboard.vue');
const RWAPickupDetails = () => import('@/views/rwa/RWAPickupDetails.vue');
const RWAWasteSummary = () => import('@/views/rwa/RWAWasteSummary.vue');
const RWACampaigns = () => import('@/views/rwa/RWACampaigns.vue');
const RWACreateCampaign = () => import('@/views/rwa/RWACreateCampaign.vue');
const RWAMonthlyPickupSummary = () => import('@/views/rwa/RWAMonthlyPickupSummary.vue');

const routes = [
  { 
    path: '/', 
    name: 'Home',
    component: Home 
  },
  { 
    path: '/register', 
    name: 'Registration',
    component: Registration 
  },
  { 
    path: '/primary-dashboard', 
    component: PrimaryUserNavbar,
    children: [
      { 
        path: '', 
        name: 'PrimaryUserDashboard',
        component: PrimaryUserDashboard 
      },
      { 
        path: 'quiz', 
        name: 'PrimaryUserQuiz',
        component: PrimaryUserQuiz 
      },
      { 
        path: 'wastelog', 
        name: 'PrimaryUserWastelog',
        component: PrimaryUserWastelog 
      },
      { 
        path: 'campaigns', 
        name: 'PrimaryUserCampaigns',
        component: PrimaryUserCampaigns 
      },
      { 
        path: 'quiz-performance', 
        name: 'PrimaryUserQuizPerformance',
        component: PrimaryUserQuizPerformance 
      },
      { 
        path: 'community-leaderboard', 
        name: 'PrimaryUserCommunityLeaderboard',
        component: PrimaryUserCommunityLeaderboard 
      },
      { 
        path: 'monthly-engagement', 
        name: 'PrimaryUserMonthlyEngagement',
        component: PrimaryUserMonthlyEngagement 
      },
      { 
        path: 'waste-summary', 
        name: 'PrimaryUserWasteSummary',
        component: PrimaryUserWasteSummary 
      }
    ]
  },
  { 
    path: '/secondary-dashboard', 
    name: 'SecondaryUserDashboard',
    component: SecondaryUserDashboard 
  },
  { 
    path: '/tertiary-dashboard', 
    name: 'TertiaryUserDashboard',
    component: TertiaryUserDashboard 
  },
  {
    path: '/rwa-dashboard',
    component: RWANavbar,
    children: [
      {
        path: '',
        name: 'RWADashboard',
        component: RWADashboard
      },
      {
        path: 'leaderboard',
        name: 'RWALeaderboard',
        component: RWALeaderboard
      },
      {
        path: 'pickup-details',
        name: 'RWAPickupDetails',
        component: RWAPickupDetails
      },
      {
        path: 'waste-summary',
        name: 'RWAWasteSummary',
        component: RWAWasteSummary
      },
      {
        path: 'campaigns',
        name: 'RWACampaigns',
        component: RWACampaigns
      },
      {
        path: 'create-campaign',
        name: 'RWACreateCampaign',
        component: RWACreateCampaign
      },
      {
        path: 'monthly-pickup-summary',
        name: 'RWAMonthlyPickupSummary',
        component: RWAMonthlyPickupSummary
      }
    ]
  },
  
  // Redirect to home if route doesn't exist
  { 
    path: '/:pathMatch(.*)*', 
    redirect: '/' 
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Scroll to top when navigating to a new route
    return { top: 0 };
  }
});

export default router;
