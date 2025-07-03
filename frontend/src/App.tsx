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
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async () => {
        const base64String = (reader.result as string).split(',')[1];
        const response = await fetch('https://api.detectaphish.com/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ body: base64String }),
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          setResult(data);
        } else {
          const errorText = await response.text();
          console.error('Error checking file:', errorText);
          setResult({ error: `Failed to check file: ${errorText}` });
        }
      };
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
