import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const checkFile = async () => {
    if (!file) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('https://api.detectaphish.com/', {
        method: 'POST',
        headers: {
          'Content-Type': file.type,
        },
        body: file,
      });
      const data = await response.json();
      console.log(data);
      setResult(data);
    } catch (error) {
      console.error('Error checking file:', error);
      setResult({ error: 'Failed to check file' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h1>Detect-a-Phish</h1>
      <div className="card">
        <input
          type="file"
          onChange={handleFileChange}
          accept=".eml,.msg,image/*"
        />
        <button onClick={checkFile} disabled={loading || !file}>
          {loading ? 'Checking...' : 'Check File'}
        </button>
        {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      </div>
    </>
  );
}

export default App;
