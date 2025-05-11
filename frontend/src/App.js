import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LearnLyticsForm from './LearnLyticsForm';

const Home = () => {
  const [typedText, setTypedText] = useState('');
  const text = 'Weelcome to LearnLytics';

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setTypedText((prevText) => prevText + text.charAt(index));  // Ensure we're appending the right character
      index += 1;
      if (index === text.length) {
        clearInterval(interval); // Stop typing once the full text is typed
      }
    }, 100); // Adjust speed (ms) here

    return () => clearInterval(interval); // Cleanup on component unmount
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center px-6">
      <h1 className="text-4xl font-bold text-lime-400 mb-4">{typedText}</h1>
      <p className="text-lg text-gray-300 max-w-xl text-center mb-6">
        LearnLytics helps you predict student performance using key academic and background data.
        Built with AI, it enables data-driven decisions in education.
      </p>
      <Link
        to="/learnlytics"
        className="bg-lime-500 hover:bg-lime-600 text-white font-semibold py-3 px-6 rounded-xl transition"
      >
        Get Started
      </Link>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/learnlytics" element={<LearnLyticsForm />} />
      </Routes>
    </Router>
  );
}

export default App;
