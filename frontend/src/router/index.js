import { createRouter, createWebHistory } from 'vue-router';

// Lazy load components for better performance
const StandardLayout = () => import('@/components/layout/StandardLayout.vue');
const Home = () => import('@/views/Home.vue');
const Registration = () => import('@/views/Registration.vue');
const SignIn = () => import('@/views/SignIn.vue');
const PrimaryUserNavbar = () => import('@/components/layout/PrimaryUserNavbar.vue');
const PrimaryUserDashboard = () => import('@/views/primary/PrimaryUserDashboard.vue');
const PrimaryUserQuiz = () => import('@/views/primary/PrimaryUserQuiz.vue');
const PrimaryUserWastelog = () => import('@/views/primary/PrimaryUserWastelog.vue');
const PrimaryUserCampaigns = () => import('@/views/primary/PrimaryUserCampaigns.vue');
const PrimaryUserQuizPerformance = () => import('@/views/primary/PrimaryUserQuizPerformance.vue');
const PrimaryUserCommunityLeaderboard = () => import('@/views/primary/PrimaryUserCommunityLeaderboard.vue');
const PrimaryUserMonthlyEngagement = () => import('@/views/primary/PrimaryUserMonthlyEngagement.vue');
const PrimaryUserWasteSummary = () => import('@/views/primary/PrimaryUserWasteSummary.vue');
const SecondaryUserNavbar = () => import('@/components/layout/SecondaryUserNavbar.vue');
const SecondaryUserDashboard = () => import('@/views/secondary/SecondaryUserDashboard.vue');
const SecondaryUserWasteSummary = () => import('@/views/secondary/SecondaryUserWasteSummary.vue');
const SecondaryUserCampaigns = () => import('@/views/secondary/SecondaryUserCampaigns.vue');
const SecondaryUserRWALeaderboard = () => import('@/views/secondary/SecondaryUserRWALeaderboard.vue');
const SecondaryUserPickupDetails = () => import('@/views/secondary/SecondaryUserPickupDetails.vue');
const SecondaryUserPickupSummary = () => import('@/views/secondary/SecondaryUserPickupSummary.vue');
const SecondaryUserDailyPickupDetails = () => import('@/views/secondary/SecondaryUserDailyPickupDetails.vue');
const SecondaryUserCreateCampaign = () => import('@/views/secondary/SecondaryUserCreateCampaign.vue');
const TertiaryUserDashboard = () => import('@/views/TertiaryUserDashboard.vue');

const routes = [
  { 
    path: '/', 
    component: StandardLayout,
    children: [
      { 
        path: '', 
        name: 'Home',
        component: Home 
      },
      { 
        path: 'register', 
        name: 'Registration',
        component: Registration 
      },
      { 
        path: 'signin', 
        name: 'SignIn',
        component: SignIn 
      }
    ]
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
    component: SecondaryUserNavbar,
    children: [
      { 
        path: '', 
        name: 'SecondaryUserDashboard',
        component: SecondaryUserDashboard 
      },
      { 
        path: 'waste-summary', 
        name: 'SecondaryUserWasteSummary',
        component: SecondaryUserWasteSummary 
      },
      { 
        path: 'campaigns', 
        name: 'SecondaryUserCampaigns',
        component: SecondaryUserCampaigns 
      },
      { 
        path: 'rwa-leaderboard', 
        name: 'SecondaryUserRWALeaderboard',
        component: SecondaryUserRWALeaderboard 
      },
      { 
        path: 'pickup-details', 
        name: 'SecondaryUserPickupDetails',
        component: SecondaryUserPickupDetails 
      },
      { 
        path: 'create-campaign', 
        name: 'SecondaryUserCreateCampaign',
        component: SecondaryUserCreateCampaign 
      },
      { 
        path: 'pickup-summary', 
        name: 'SecondaryUserPickupSummary',
        component: SecondaryUserPickupSummary 
      },
      { 
        path: 'daily-pickup-details', 
        name: 'SecondaryUserDailyPickupDetails',
        component: SecondaryUserDailyPickupDetails 
      }
    ]
  },
  { 
    path: '/tertiary-dashboard', 
    name: 'TertiaryUserDashboard',
    component: TertiaryUserDashboard 
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
