import React, { useState, useEffect } from 'react';
import './BuyBlackGuide.css'; // You'll need to create this CSS file

const API_BASE_URL = 'http://localhost:8000'; // Change to your API server URL

const BuyBlackGuide = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "👋 Hi! I'm your BuyBlack City Guide. Ask me about Black-owned restaurants, cultural sites, or help planning your trip to Oakland!", sender: 'bot' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [businesses, setBusinesses] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('restaurant');
  const [searchKeyword, setSearchKeyword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Chat functionality
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          conversation_id: 'react_chat'
        })
      });

      const data = await response.json();
      
      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot'
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Business search functionality
  const searchBusinesses = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/businesses/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          category: selectedCategory,
          keyword: searchKeyword,
          limit: 10
        })
      });

      const data = await response.json();
      setBusinesses(data.businesses || []);
    } catch (error) {
      console.error('Error searching businesses:', error);
      setBusinesses([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Quick actions
  const quickActions = [
    { label: '🍽️ Find Restaurants', action: () => setInputMessage('Find Black-owned restaurants in Oakland') },
    { label: '🥖 Find Bakeries', action: () => setInputMessage('Find Black-owned bakeries in Oakland') },
    { label: '🧳 Plan Trip', action: () => setInputMessage('Plan a 2-day cultural trip to Oakland') },
    { label: '🏛️ Cultural Sites', action: () => setInputMessage('What are the most important cultural landmarks in Oakland?') }
  ];

  useEffect(() => {
    searchBusinesses();
  }, []);

  return (
    <div className="buyblack-guide">
      <div className="header">
        <h1>🏙️ BuyBlack City Guide</h1>
        <p>Discover Black-owned businesses and cultural experiences in Oakland</p>
      </div>

      <div className="main-container">
        {/* Chat Section */}
        <div className="chat-section">
          <h3>💬 Chat with the Guide</h3>
          
          <div className="chat-container">
            {messages.map(message => (
              <div key={message.id} className={`message ${message.sender}-message`}>
                {message.text}
              </div>
            ))}
            {isLoading && (
              <div className="message bot-message loading">
                Thinking...
              </div>
            )}
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask about Black-owned businesses, cultural sites, or trip planning..."
            />
            <button onClick={sendMessage} disabled={isLoading}>
              Send
            </button>
          </div>

          <div className="quick-actions">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={action.action}
                className="quick-action-btn"
              >
                {action.label}
              </button>
            ))}
          </div>
        </div>

        {/* Business Search Section */}
        <div className="search-section">
          <h3>🔍 Search Businesses</h3>
          
          <div className="search-controls">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <option value="restaurant">Restaurants</option>
              <option value="bakery">Bakeries</option>
              <option value="coffee">Coffee Shops</option>
              <option value="barber">Barbershops</option>
              <option value="beauty">Beauty Services</option>
              <option value="retail">Retail Shops</option>
            </select>
            
            <input
              type="text"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              placeholder="Optional keyword..."
            />
            
            <button onClick={searchBusinesses} disabled={isLoading}>
              {isLoading ? 'Searching...' : 'Search'}
            </button>
          </div>

          <div className="business-results">
            {businesses.length > 0 ? (
              businesses.map((business, index) => (
                <div key={index} className="business-card">
                  <div className="business-name">{business.name || 'N/A'}</div>
                  <div className="business-type">{business.type || 'N/A'}</div>
                  <div className="business-address">{business.address || 'N/A'}</div>
                  {business.phone && <div>📞 {business.phone}</div>}
                  {business.website && (
                    <div>🌐 <a href={business.website} target="_blank" rel="noopener noreferrer">Visit Website</a></div>
                  )}
                  {business.rating && (
                    <div>⭐ {business.rating}/5 ({business.reviews} reviews)</div>
                  )}
                </div>
              ))
            ) : (
              <div className="no-results">
                {isLoading ? 'Searching businesses...' : 'No businesses found. Try a different category or keyword.'}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BuyBlackGuide;
