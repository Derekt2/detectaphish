import { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const checkUrl = async () => {
    setLoading(true);
    try {
      const response = await fetch('https://api.detectaphish.com/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      console.log(data);
      setResult(data);
    } catch (error) {
      console.error('Error checking URL:', error);
      setResult({ error: 'Failed to check URL' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h1>Detect-a-Phish</h1>
      <div className="card">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL to check"
        />
        <button onClick={checkUrl} disabled={loading}>
          {loading ? 'Checking...' : 'Check URL'}
        </button>
        {result && (
          <pre>{JSON.stringify(result, null, 2)}</pre>
        )}
      </div>
    </>
  );
}

export default App;
