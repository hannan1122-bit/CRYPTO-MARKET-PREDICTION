'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import '@fontsource/orbitron';

interface DataPoint {
  timestamp: string;
  close: number;
  highlightedClose?: number | null;
}

export default function Page() {
  const [data, setData] = useState<{ original: DataPoint[]; predicted: DataPoint[] }>({
    original: [],
    predicted: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showNav, setShowNav] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    axios
      .get('http://localhost:5000/predict')
      .then((res) => {
        const rawData = res.data;
        const total = rawData.predicted.length;

        const highlightedPredicted = rawData.predicted.map(
          (point: DataPoint, index: number) => ({
            ...point,
            highlightedClose: index >= total - 10 ? point.close : null,
          })
        );

        setData({
          original: rawData.original,
          predicted: highlightedPredicted,
        });
        setLoading(false);
      })
      .catch((err) => {
        setError('Failed to load prediction data.');
        setLoading(false);
        console.error(err);
      });
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      setShowNav(currentScrollY < lastScrollY || currentScrollY < 10);
      setLastScrollY(currentScrollY);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [lastScrollY]);

  const formatTimestamp = (timestamp: string) =>
    new Date(timestamp).toLocaleString('en-GB', {
      hour: '2-digit',
      minute: '2-digit',
      day: 'numeric',
      month: 'short',
    });

  const last10 = data.predicted.slice(-10);
  const allPrices = [...data.original, ...data.predicted].map((d) => d.close);
  const minY = Math.min(...allPrices);
  const maxY = Math.max(...allPrices);
  const yPadding = (maxY - minY) * 0.08;
  const yDomain: [number, number] = [minY - yPadding, maxY + yPadding];

  return (
    <div className="relative min-h-screen bg-[#0d1117] text-gray-300 font-orbitron">
      {/* Background Layer */}
      <div className="absolute inset-0 flex flex-row items-center justify-center pointer-events-none z-0 opacity-15 select-none px-2 sm:px-4 md:px-8 lg:px-16 py-2 sm:py-4 md:py-6 lg:py-8 space-x-4 sm:space-x-6 md:space-x-10 lg:space-x-14">
        <span className="text-[200px] sm:text-[300px] md:text-[400px] lg:text-[450px] font-extrabold text-purple-100 m-1 sm:m-2 md:m-4">🧠</span>
        <span className="text-[100px] sm:text-[150px] md:text-[200px] lg:text-[250px] font-extrabold text-white m-1 sm:m-2 md:m-4">+</span>
        <span className="text-[150px] sm:text-[250px] md:text-[300px] lg:text-[350px] font-extrabold text-yellow-400 m-1 sm:m-2 md:m-4">₿</span>
      </div>



      {/* Sticky Navbar */}
      <nav
        className={`fixed top-0 left-0 right-0 z-50 py-4 px-4 sm:px-6 transition-transform duration-300 ease-in-out bg-gray-400 bg-opacity-95 border-b-2 border-red-600 shadow-md ${showNav ? 'translate-y-0' : '-translate-y-full'
          }`}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex-shrink-0 text-2xl sm:text-3xl">🪙</div>
          <h1 className="text-red-700 text-xl sm:text-2xl md:text-3xl font-extrabold tracking-wider text-center flex-grow mx-2 sm:mx-4">
            DOCTOR’S CRYPTO PREDICTION
          </h1>
          <div className="flex-shrink-0 text-2xl sm:text-3xl">⛰️</div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto px-4 pt-28 pb-8 relative z-10">
        {loading ? (
          <div className="text-center text-xl py-20 text-white">Loading data...</div>
        ) : error ? (
          <div className="text-center text-red-400 text-lg py-20">{error}</div>
        ) : (
          <>
            {/* Prediction List */}
            <section className="mb-10">
              <h2 className="text-2xl font-semibold text-center mb-4">
                Next 10 Hour Predictions
              </h2>

              {last10.length > 0 && (
                <div className="mb-4 text-center text-white text-sm">
                  <span className="bg-red-600 text-white px-4 py-2 rounded shadow-lg font-semibold">
                    Current Time: {formatTimestamp(new Date(new Date(last10[0].timestamp).getTime() - 3600000))}
                  </span>
                </div>
              )}

              <ul className="grid md:grid-cols-5 grid-cols-2 gap-4 bg-[#161b22] p-4 rounded-lg shadow-lg">
                {last10.map((point, index) => (
                  <li
                    key={index}
                    className="p-3 border-2 border-red-500 rounded-lg text-center bg-white text-red-700 font-semibold hover:bg-red-100 transition"
                  >
                    <div className="text-sm font-medium">
                      {formatTimestamp(point.timestamp)}
                    </div>
                    <div className="text-xl font-bold">{point.close.toFixed(2)} USD</div>
                  </li>
                ))}
              </ul>
            </section>

            {/* Description */}
            <section className="mb-10 max-w-3xl mx-auto text-center px-4">
              <p className="text-lg leading-relaxed text-gray-200">
                Welcome to Doctor’s Crypto Prediction – your intelligent window into the
                future of crypto! Using advanced machine learning models and real-time
                analysis, we forecast Bitcoin trends to help you make smarter decisions.
                Let data drive your strategy. Navigate your crypto journey — with
                foresight, not guesswork.
              </p>
            </section>

            {/* Original Prices Graph */}
            <section className="mb-14">
              <h2 className="text-3xl font-bold text-red-600 text-center mb-2">Original Prices</h2>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data.original} margin={{ top: 60, right: 30, left: 60, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={formatTimestamp}
                    angle={-30}
                    height={80}
                    textAnchor="end"
                    stroke="#ccc"
                    minTickGap={20}
                  />
                  <YAxis
                    domain={yDomain}
                    tickFormatter={(tick) => `${tick.toLocaleString()} USD`}
                    stroke="#ccc"
                  />
                  <Tooltip
                    labelFormatter={formatTimestamp}
                    contentStyle={{
                      backgroundColor: '#222',
                      borderColor: '#666',
                      color: '#fff',
                    }}
                    labelStyle={{ color: '#fff', fontWeight: 'bold' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="close"
                    name="Original Price"
                    stroke="#1f77b4"
                    dot={false}
                    strokeWidth={2}
                    animationDuration={0}
                  />
                </LineChart>
              </ResponsiveContainer>
              <div className="text-center text-sm text-blue-400 mt-2">
                Legend: Blue Line = Original BTC Price
              </div>
            </section>

            {/* Predicted Prices Graph */}
            <section className="mb-14">
              <h2 className="text-3xl font-bold text-red-600 text-center mb-2">Predicted Prices</h2>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data.predicted} margin={{ top: 60, right: 30, left: 60, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={formatTimestamp}
                    angle={-30}
                    height={80}
                    textAnchor="end"
                    stroke="#ccc"
                    minTickGap={20}
                  />
                  <YAxis
                    domain={yDomain}
                    tickFormatter={(tick) => `${tick.toLocaleString()} USD`}
                    stroke="#ccc"
                  />
                  <Tooltip
                    labelFormatter={formatTimestamp}
                    contentStyle={{
                      backgroundColor: '#222',
                      borderColor: '#666',
                      color: '#fff',
                    }}
                    labelStyle={{ color: '#fff', fontWeight: 'bold' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="close"
                    name="Predicted Price"
                    stroke="#2ca02c"
                    dot={false}
                    strokeWidth={2}
                    animationDuration={0}
                  />
                  <Line
                    type="monotone"
                    dataKey="highlightedClose"
                    name="Last 10 Hour Forecast"
                    stroke="#ff4136"
                    dot={false}
                    strokeWidth={3}
                    animationDuration={0}
                  />
                </LineChart>
              </ResponsiveContainer>
              <div className="text-center text-sm text-green-400 mt-2">
                Legend: Green = Predicted | Red = Last 10-Hour Forecast
              </div>
            </section>
          </>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white bg-opacity-90 text-black p-4 text-center z-10 shadow-inner">
        <p>
          © {new Date().getFullYear()} Doctor's Crypto Prediction — All rights reserved.
        </p>
      </footer>
    </div>
  );
}
