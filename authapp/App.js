import React, { Component } from 'react';
import Router from './src/Router';


export default class App extends Component {
  render() {
    return (
      <Router />
    );
  }

  componentWillMount() {
    axios.defaults.baseURL = '127.0.0.1:8000/api';
    axios.defaults.timeout = 1500;
  }

}
