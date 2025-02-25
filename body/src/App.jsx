import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { FileText, Link } from 'lucide-react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [markdown, setMarkdown] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMarkdown('');

    try {
      const response = await axios.get('http://127.0.0.1:8000/summary');
      setMarkdown(response.data.summary);
    } catch (err) {
      setError(
        axios.isAxiosError(err)
          ? err.response?.data?.message || err.message
          : 'An error occurred'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-group">
          <Link size={20} className="input-icon" />
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter markdown file URL"
            required
            className="url-input"
          />
        </div>
        <button type="submit" className="submit-button" disabled={loading}>
          Get Summary
        </button>
      </form>

      {loading && (
        <div className="loading">
          <FileText size={24} style={{ margin: '0 auto 1rem' }} />
          <p>Loading markdown content...</p>
        </div>
      )}

      {error && (
        <div className="error">
          <p>Error: {error}</p>
        </div>
      )}

      {markdown && (
        <div className="markdown-content">
          <ReactMarkdown>{markdown}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;