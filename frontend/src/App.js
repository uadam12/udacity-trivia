import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';

const App = () => 
(<div className='App'>
    <Header path />
    <Routes>
        <Route path="/" element={ <QuestionView /> } />
        <Route path="add" element={ <FormView /> } />
        <Route path="play" element={ <QuizView /> } />
    </Routes>

  </div>
);

export default App;