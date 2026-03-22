# SETUP.md

## Prerequisites

1. **Node.js**: Make sure you have Node.js installed on your system. You can download it from [Node.js Official Website](https://nodejs.org/).
2. **Git**: Ensure that Git is installed and available on your command line. Download it from [Git Official Website](https://git-scm.com/).

## Installation Steps

1. **Clone the Repository**  
   Open your terminal and run:
   ```bash
   git clone https://github.com/ballales1984-wq/ManagerSchool.git
   cd ManagerSchool
   ```

2. **Install Dependencies**  
   Run the following command to install the necessary packages:
   ```bash
   npm install
   ```

3. **Environment Configuration**  
   Create a `.env` file in the root directory and provide the required configurations such as:
   ```env
   DATABASE_URL=<your_database_url>
   PORT=3000
   ```
   Replace `<your_database_url>` with your actual database URL.

## Quick Verification

After completing the installation and setup, you can run the application to verify everything is working:

```bash
npm start
```

Visit `http://localhost:3000` in your browser to confirm that the application is running successfully.