# Waste Management System - Frontend

This is the frontend for the Waste Management System, built with Vue 3, Vite, and Pinia for state management. The application provides a user interface for managing waste collection and monitoring.

## Prerequisites

- Node.js (v16 or higher recommended)
- npm (v8 or higher) or yarn
- Git

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd waste-management-system/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

## Available Scripts

### Development Server

Start the development server with hot-reload:
```bash
npm run dev
# or
yarn dev
```
The application will be available at `http://localhost:5173`

### Building for Production

Create a production build:
```bash
npm run build
# or
yarn build
```

The build artifacts will be stored in the `dist/` directory.

### Preview Production Build

To preview the production build locally:
```bash
npm run preview
# or
yarn preview
```

## Project Structure

```
frontend/
├── public/          # Static files
├── src/
│   ├── assets/      # Assets like images, styles
│   ├── components/  # Reusable Vue components
│   ├── router/      # Vue Router configuration
│   ├── stores/      # Pinia stores
│   ├── views/       # Page components
│   ├── App.vue      # Root Vue component
│   └── main.js      # Application entry point
├── .gitignore
├── index.html
├── package.json
└── vite.config.js
```

## Technologies Used

- Vue 3 - Progressive JavaScript framework
- Vite - Next Generation Frontend Tooling
- Pinia - Intuitive state management
- Vue Router - Official router for Vue.js
- Bootstrap 5 - CSS framework
- Chart.js - For data visualization
- Axios - HTTP client

## Browser Support

The application is tested on the latest versions of:
- Chrome
- Firefox
- Edge
- Safari

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.