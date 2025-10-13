# 🌐 Website Integration Guide for BuyBlack City Guide

This guide shows you how to integrate your BuyBlack City Guide agency into your website using different methods.

## 🚀 **Method 1: REST API (Recommended)**

### **Step 1: Start the API Server**

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python api_server.py
```

The API will be available at `http://localhost:8000`

### **Step 2: API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Chat with the agency |
| `/api/businesses/search` | POST | Search Black-owned businesses |
| `/api/itinerary/create` | POST | Create personalized itineraries |
| `/api/businesses/categories` | GET | Get available business categories |
| `/api/cities` | GET | Get supported cities |

### **Step 3: Integration Examples**

#### **HTML/JavaScript Integration**
- Use the provided `website_integration_example.html` file
- Copy the HTML, CSS, and JavaScript into your website
- Update the `API_BASE_URL` to point to your server

#### **React Integration**
- Use the provided `react_integration_example.jsx` and `BuyBlackGuide.css`
- Import the component into your React app
- Update the `API_BASE_URL` constant

#### **WordPress Integration**
```php
// Add this to your WordPress theme's functions.php
function buyblack_chat_shortcode($atts) {
    $api_url = 'http://your-api-server.com';
    // Include the chat HTML and JavaScript
    return '<div id="buyblack-chat">...</div>';
}
add_shortcode('buyblack_chat', 'buyblack_chat_shortcode');
```

## 🔧 **Method 2: Direct Integration (Advanced)**

### **Embed the Agency Directly**

```python
# In your Django/Flask app
from agency import create_agency
import asyncio

async def get_buyblack_response(message):
    agency = create_agency()
    result = await agency.get_response(message)
    return result.final_output if hasattr(result, 'final_output') else str(result)

# Django view example
def chat_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = asyncio.run(get_buyblack_response(message))
        return JsonResponse({'response': response})
```

## 🌍 **Method 3: Cloud Deployment**

### **Deploy API to Cloud**

#### **Railway (Easiest)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

#### **Heroku**
```bash
# Create Procfile
echo "web: uvicorn api_server:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git add .
git commit -m "Deploy BuyBlack API"
git push heroku main
```

#### **AWS/GCP/Azure**
- Use Docker containers
- Deploy with load balancers
- Set up environment variables for API keys

## 📱 **Method 4: Mobile App Integration**

### **React Native**
```javascript
const API_BASE_URL = 'https://your-api-server.com';

const searchBusinesses = async (category) => {
  const response = await fetch(`${API_BASE_URL}/api/businesses/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ category, limit: 10 })
  });
  return response.json();
};
```

### **Flutter**
```dart
import 'package:http/http.dart' as http;

Future<List<Business>> searchBusinesses(String category) async {
  final response = await http.post(
    Uri.parse('https://your-api-server.com/api/businesses/search'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({'category': category, 'limit': 10}),
  );
  
  if (response.statusCode == 200) {
    return Business.fromJsonList(json.decode(response.body)['businesses']);
  }
  throw Exception('Failed to load businesses');
}
```

## 🔐 **Security Considerations**

### **Production Setup**
1. **CORS Configuration**: Update CORS settings for production
2. **API Keys**: Store API keys in environment variables
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Authentication**: Add API authentication if needed
5. **HTTPS**: Always use HTTPS in production

### **Environment Variables**
```bash
# .env file
OPENAI_API_KEY=your_openai_key
GOOGLE_PLACES_API_KEY=your_google_key
ALLOWED_ORIGINS=https://yourwebsite.com,https://www.yourwebsite.com
```

## 📊 **Analytics & Monitoring**

### **Add Analytics**
```javascript
// Track user interactions
function trackChatMessage(message) {
  gtag('event', 'chat_message', {
    'event_category': 'engagement',
    'event_label': message.substring(0, 50)
  });
}

function trackBusinessSearch(category) {
  gtag('event', 'business_search', {
    'event_category': 'search',
    'event_label': category
  });
}
```

### **Monitor API Usage**
- Set up logging for API calls
- Monitor response times
- Track error rates
- Set up alerts for high usage

## 🎨 **Customization Options**

### **Styling**
- Customize colors, fonts, and layout
- Add your brand colors to the CSS
- Modify the chat interface design
- Add animations and transitions

### **Features**
- Add user accounts and favorites
- Implement location-based search
- Add social sharing features
- Create custom business categories

### **Data Sources**
- Add more cities beyond Oakland
- Integrate additional APIs (Yelp, Foursquare)
- Add event calendars
- Include user reviews and ratings

## 🚀 **Quick Start Checklist**

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set up environment variables (API keys)
- [ ] Start the API server: `python api_server.py`
- [ ] Test the API endpoints
- [ ] Choose integration method (HTML/React/Direct)
- [ ] Customize styling and features
- [ ] Deploy to production
- [ ] Set up monitoring and analytics

## 📞 **Support**

For questions or issues:
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the example files provided
3. Test individual components before full integration
4. Monitor logs for error messages

---

**Happy coding! Your BuyBlack City Guide is ready to help users discover amazing Black-owned businesses! 🎉**
