import React from 'react';
import { render } from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import { Provider } from 'react-redux'
import { applyMiddleware, createStore, combineReducers, compose } from 'redux'
import thunk from 'redux-thunk'
import App from './app.js';
import reducers from './reducer'

const reducer = combineReducers(reducers)
const store = createStore(
  reducer,
  compose(applyMiddleware(thunk), window.devToolsExtension ? window.devToolsExtension() : f => f)
)

render( <AppContainer><Provider store={store}><App/></Provider></AppContainer>, document.getElementById("app"));

if (module && module.hot) {
  module.hot.accept('./app.js', () => {
    const App = require('./app.js').default;
    render(
      <AppContainer>
        <Provider store={store}><App/></Provider>
      </AppContainer>,
      document.getElementById("app")  
    );
  });
}
