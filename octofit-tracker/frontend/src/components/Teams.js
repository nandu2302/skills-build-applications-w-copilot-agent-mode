import React, { useEffect, useState } from 'react';

const getBaseUrl = () => {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  if (codespace && codespace.trim()) {
    return `https://${codespace.trim()}-8000.app.github.dev/api/`;
  }
  return 'http://localhost:8000/api/';
};

export default function Teams() {
  const [items, setItems] = useState([]);
  const [endpoint, setEndpoint] = useState('');
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selected, setSelected] = useState(null);

  const fetchData = () => {
    const base = getBaseUrl();
    const url = base + 'teams/';
    setEndpoint(url);
    console.log('Teams endpoint:', url);
    setLoading(true);

    fetch(url, { headers: { Accept: 'application/json' } })
      .then((r) => r.json())
      .then((data) => {
        console.log('Teams data:', data);
        const list = data && data.results ? data.results : data;
        setItems(Array.isArray(list) ? list : []);
      })
      .catch((err) => console.error('Teams fetch error:', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchData(); }, []);

  const headers = items.length && typeof items[0] === 'object' ? Object.keys(items[0]) : ['value'];
  const openModal = (item) => { setSelected(item); setShowModal(true); };

  return (
    <div className="card">
      <div className="card-body">
        <h2 className="card-title">Teams</h2>
        <p className="text-muted">Endpoint: <code>{endpoint}</code></p>
        <div className="mb-3">
          <button className="btn btn-primary me-2" onClick={fetchData} disabled={loading}>{loading ? 'Loading...' : 'Refresh'}</button>
        </div>

        {items.length === 0 ? (<p className="text-muted">No items found.</p>) : (
          <div className="table-responsive">
            <table className="table table-striped table-bordered">
              <thead>
                <tr>
                  {headers.map(h => <th key={h}>{h}</th>)}
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((it, idx) => (
                  <tr key={idx}>
                    {headers.map(h => <td key={h}>{typeof it === 'object' ? JSON.stringify(it[h]) : String(it)}</td>)}
                    <td><button className="btn btn-sm btn-outline-primary" onClick={() => openModal(it)}>View</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showModal && (
        <div>
          <div className="modal show d-block" tabIndex={-1} role="dialog">
            <div className="modal-dialog modal-lg" role="document">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Team details</h5>
                  <button type="button" className="btn-close" aria-label="Close" onClick={() => setShowModal(false)} />
                </div>
                <div className="modal-body">
                  <pre>{JSON.stringify(selected, null, 2)}</pre>
                </div>
                <div className="modal-footer">
                  <button className="btn btn-secondary" onClick={() => setShowModal(false)}>Close</button>
                </div>
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show" />
        </div>
      )}
    </div>
  );
}
