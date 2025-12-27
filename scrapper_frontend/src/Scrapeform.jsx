import React, { useState } from 'react';
import axios from 'axios';

const baseUrl = "https://scrapper-backend-l28z.onrender.com";



const ScrapeForm = () => {
  const [festUrl, setFestUrl] = useState('');
  const [festName, setFestName] = useState('');
  const [college, setCollege] = useState('');
  const [year, setYear] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');

    try {
      console.log('POSTing to:', `${baseUrl}/api/scrape`);

      const res = await axios.post(`${baseUrl}/api/scrape`, {
        url: festUrl,
        fest_name: festName,
        college: college,
        year: year,
      });

      setResponse(res.data.message || JSON.stringify(res.data));
    } catch (err) {
      console.error(err);
      setResponse('Error connecting to backend');

    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: '#000', color: '#fff', minHeight: '100vh', padding: '2rem' }}>
      <div style={{ position: 'absolute', top: 10, right: 20 }}>
        <a href="https://xyz" target="_blank" rel="noopener noreferrer" style={{ color: '#0ff' }}>
          View Database
        </a>
      </div>

      <h2>Scrape Fest Sponsors</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', maxWidth: '400px' }}>
        <input type="text" placeholder="Fest URL" value={festUrl} onChange={(e) => setFestUrl(e.target.value)} required />
        <input type="text" placeholder="Fest Name" value={festName} onChange={(e) => setFestName(e.target.value)} required />
        <input type="text" placeholder="College Name" value={college} onChange={(e) => setCollege(e.target.value)} required />
        <input type="number" placeholder="Fest Year" value={year} onChange={(e) => setYear(e.target.value)} required />
        <button type="submit" disabled={loading} style={{ marginTop: '1rem' }}>
          {loading ? 'Scraping...' : 'Submit'}
        </button>
      </form>

      {response && (
        <div style={{ marginTop: '2rem', whiteSpace: 'pre-wrap' }}>
          <h4>Response:</h4>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default ScrapeForm;
