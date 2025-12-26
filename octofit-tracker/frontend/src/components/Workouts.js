import React, { useEffect, useState } from 'react';

const getBaseUrl = () => {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  if (codespace && codespace.trim()) {
    return `https://${codespace.trim()}-8000.app.github.dev/api/`;
  }
  return 'http://localhost:8000/api/';
};

export default function Workouts() {
  const [items, setItems] = useState([]);
  const [endpoint, setEndpoint] = useState('');

  useEffect(() => {
    const base = getBaseUrl();
    const url = base + 'workouts/';
    setEndpoint(url);
    console.log('Workouts endpoint:', url);

    fetch(url, { headers: { Accept: 'application/json' } })
      .then((r) => r.json())
      .then((data) => {
        console.log('Workouts data:', data);
        const list = data && data.results ? data.results : data;
        setItems(Array.isArray(list) ? list : []);
      })
      .catch((err) => console.error('Workouts fetch error:', err));
  }, []);

  return (
    <div>
      <h2>Workouts</h2>
      <p className="text-muted">Endpoint: <code>{endpoint}</code></p>
      <p>Found: {items.length}</p>
      <ul className="list-group">
        {items.map((it, idx) => (
          <li key={idx} className="list-group-item">
            <pre style={{ margin: 0 }}>{JSON.stringify(it, null, 2)}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
}
