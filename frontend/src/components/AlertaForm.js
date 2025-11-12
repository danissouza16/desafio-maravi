import React, { useState } from 'react';
import { createAlerta } from '../api/apiService';

function AlertaForm() {
    const [email, setEmail] = useState('');
    const [linha, setLinha] = useState('');
    const [latitude, setLatitude] = useState(''); //ponto_partida_lat
    const [longitude, setLongitude] = useState(''); //ponto_partida_lon
    const [inicio, setInicio] = useState('08:00'); //horario_inicio
    const [fim, setFim] = useState('09:00'); //horario_fim
    const [mensagem, setMensagem] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setMensagem('Enviando...');

        const alertaData = {
            email_usuario: email,
            linha_onibus: linha,
            ponto_partida_lat: parseFloat(latitude),
            ponto_partida_lon: parseFloat(longitude),
            horario_inicio: inicio,
            horario_fim: fim,
        };

        try {
            const response = await createAlerta(alertaData);
            console.log('Alerta criado:', response.data);
            setMensagem({
              texto: `Alerta criado com sucesso para a linha ${response.data.linha_onibus}!`,
              tipo: 'success'
            });
            
            //limpar o formulário após o envio
            setEmail('');
            setLinha('');
            setLatitude('');
            setLongitude('');
        } catch (error) {
            console.error('Erro ao criar alerta:', error);
            const errorMsg = error.response?.data?.detail || 'Erro ao criar alerta. Tente novamente.';
            setMensagem({
              texto: 'Erro: ${errorMsg}',
              tipo: 'error'
            });
        }
    };
    return (
        <div className="form-container">
      <h2>Criar Novo Alerta de Ônibus</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Seu Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Linha do Ônibus (ex: 474):</label>
          <input
            type="text"
            value={linha}
            onChange={(e) => setLinha(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Ponto de Partida (Latitude):</label>
          <input
            type="number"
            step="any"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
            placeholder="-22.9068"
            required
          />
        </div>
        <div className="form-group">
          <label>Ponto de Partida (Longitude):</label>
          <input
            type="number"
            step="any"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
            placeholder="-43.1729"
            required
          />
        </div>
        <div className="form-group-inline">
          <div className="form-group">
            <label>Janela de Início:</label>
            <input
              type="time"
              value={inicio}
              onChange={(e) => setInicio(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Janela de Fim:</label>
            <input
              type="time"
              value={fim}
              onChange={(e) => setFim(e.target.value)}
              required
            />
          </div>
        </div>
        <button type="submit">Criar Alerta</button>
      </form>
      {/* Exibe a mensagem de sucesso ou erro */}
      {mensagem && <p className="feedback-message ${mensagem.tipo}">{mensagem.texto}</p>}
    </div>
  );
}
export default AlertaForm;
