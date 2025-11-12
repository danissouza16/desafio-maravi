import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Correção para o ícone do marcador padrão do Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

function Dashboard() {
  const [linha, setLinha] = useState('474');
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);

  const buscarOnibus = async () => {
    setLoading(true);
    setErro(null);
    try {
      // Usa a URL do .env
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
      const response = await axios.get(`${apiUrl}/onibus/${linha}`);
      setDados(response.data);
    } catch (error) {
      console.error("Erro ao buscar ônibus:", error);
      setErro("Erro ao buscar dados. Verifique se o backend está rodando.");
    } finally {
      setLoading(false);
    }
  };

  // Busca dados automaticamente ao abrir a página
  useEffect(() => {
    buscarOnibus();
    // Opcional: Atualizar a cada 30 segundos
    const intervalo = setInterval(buscarOnibus, 30000);
    return () => clearInterval(intervalo);
  }, []);

  return (
    <div className="container">
      <h2>Monitoramento em Tempo Real</h2>
      
      <div className="form-group-inline">
        <input 
          type="text" 
          value={linha} 
          onChange={(e) => setLinha(e.target.value)} 
          placeholder="Digite a linha (ex: 474)"
        />
        <button onClick={buscarOnibus} disabled={loading}>
          {loading ? 'Buscando...' : 'Atualizar'}
        </button>
      </div>

      {erro && <p className="feedback-message error">{erro}</p>}

      {dados && (
        <div>
          <p><strong>Total de Veículos Encontrados:</strong> {dados.total}</p>
          
          {/*mapa*/}
          <div className="map-container" style={{ height: '400px', marginBottom: '20px', border: '1px solid #ccc' }}>
            <MapContainer center={[-22.9068, -43.1729]} zoom={12} style={{ height: '100%', width: '100%' }}>
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; OpenStreetMap contributors'
              />
              {dados.veiculos.map((bus, index) => (
                <Marker 
                  key={index} 
                  position={[bus.latitude, bus.longitude]}
                >
                  <Popup>
                    <strong>Linha: {bus.linha}</strong><br/>
                    Velocidade: {bus.velocidade} km/h
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>

          {/*tabela */}
          {dados.veiculos.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Linha</th>
                  <th>Latitude</th>
                  <th>Longitude</th>
                  <th>Velocidade</th>
                  <th>Data/Hora</th>
                </tr>
              </thead>
              <tbody>
                {dados.veiculos.map((bus, index) => (
                  <tr key={index}>
                    <td>{bus.linha}</td>
                    <td>{bus.latitude}</td>
                    <td>{bus.longitude}</td>
                    <td>{bus.velocidade || 0} km/h</td>
                    <td>{bus.datahora}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum ônibus encontrado para esta linha no momento.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default Dashboard;