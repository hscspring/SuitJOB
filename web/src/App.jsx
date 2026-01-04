import React, { useState, useEffect } from 'react';
import { initModel, generateWords, calcScore, cn } from './utils/logic';

const LoadingScreen = () => (
  <div className="flex flex-col items-center justify-center h-screen space-y-4">
    <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
    <div className="text-xl text-indigo-300 font-light tracking-widest animate-pulse">LOADING MODEL</div>
  </div>
);

const Home = ({ onStart }) => (
  <div className="text-center space-y-12 max-w-2xl mx-auto animate-fade-in">
    <div className="space-y-4">
      <h1 className="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-500 tracking-tighter">
        SuitJOB
      </h1>
      <p className="text-xl md:text-2xl text-slate-400 font-light">
        Discover your perfect career match through data-driven analysis.
      </p>
    </div>
    <button
      onClick={onStart}
      className="group relative px-8 py-4 bg-indigo-600 rounded-full font-bold text-lg hover:bg-indigo-500 transition-all duration-300 shadow-lg hover:shadow-indigo-500/25 active:scale-95"
    >
      <span className="relative z-10 flex items-center space-x-2">
        <span>START ANALYSIS</span>
        <span className="group-hover:translate-x-1 transition-transform">→</span>
      </span>
    </button>
    <p className="text-sm text-slate-600">Based on analysis of 30,000+ real job postings.</p>
  </div>
);

const Tag = ({ children, selected, onClick, type }) => (
  <button
    onClick={onClick}
    className={cn(
      "px-4 py-2 rounded-xl text-sm md:text-base font-medium transition-all duration-200 border",
      selected
        ? type === 'like' ? "bg-pink-500/20 border-pink-500 text-pink-300 shadow-[0_0_15px_rgba(236,72,153,0.3)]"
          : "bg-indigo-500/20 border-indigo-500 text-indigo-300 shadow-[0_0_15px_rgba(99,102,241,0.3)]"
        : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500 hover:bg-slate-800"
    )}
  >
    {children}
  </button>
);

const Select = ({ words, choices, setChoices, onAnalyze }) => {
  const handleToggle = (type, item) => {
    const current = choices[type];
    const exists = current.find(x => x.word === item.word);
    let next;
    if (exists) {
      next = current.filter(x => x.word !== item.word);
    } else {
      next = [...current, item];
    }
    setChoices({ ...choices, [type]: next });
  };

  const hasSelection = choices.like.length > 0 || choices.cando.length > 0;

  return (
    <div className="w-full max-w-5xl mx-auto space-y-12 animate-slide-up pb-20">
      <header className="flex justify-between items-center sticky top-0 md:relative bg-slate-900/90 backdrop-blur-sm z-20 py-4 border-b border-slate-800 md:border-none">
        <h2 className="text-2xl font-bold text-slate-200">Select Keywords</h2>
        <div className="text-sm text-slate-400">
          <span className="text-pink-400 font-bold">{choices.like.length}</span> Likes &bull; {' '}
          <span className="text-indigo-400 font-bold">{choices.cando.length}</span> Skills
        </div>
      </header>

      <div className="space-y-8">
        <section>
          <h3 className="text-pink-400 text-sm font-bold uppercase tracking-wider mb-6 flex items-center">
            <span className="w-2 h-8 bg-pink-500 rounded-full mr-3"></span>
            What interests you?
          </h3>
          <div className="flex flex-wrap gap-3">
            {words.like.map(item => (
              <Tag
                key={item.word}
                type="like"
                selected={!!choices.like.find(x => x.word === item.word)}
                onClick={() => handleToggle('like', item)}
              >
                {item.word}
              </Tag>
            ))}
          </div>
        </section>

        <section>
          <h3 className="text-indigo-400 text-sm font-bold uppercase tracking-wider mb-6 flex items-center">
            <span className="w-2 h-8 bg-indigo-500 rounded-full mr-3"></span>
            What can you do?
          </h3>
          <div className="flex flex-wrap gap-3">
            {words.cando.map(item => (
              <Tag
                key={item.word}
                type="cando"
                selected={!!choices.cando.find(x => x.word === item.word)}
                onClick={() => handleToggle('cando', item)}
              >
                {item.word}
              </Tag>
            ))}
          </div>
        </section>
      </div>

      <div className="fixed bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-slate-900 via-slate-900 to-transparent z-30 flex justify-center">
        <button
          onClick={onAnalyze}
          disabled={!hasSelection}
          className="disabled:opacity-50 disabled:cursor-not-allowed px-12 py-4 bg-white text-slate-900 rounded-full font-bold text-lg hover:bg-slate-200 transition-all shadow-[0_0_20px_rgba(255,255,255,0.2)]"
        >
          Get Matches
        </button>
      </div>
    </div>
  );
};

const Result = ({ results, onRestart }) => (
  <div className="w-full max-w-3xl mx-auto space-y-12 animate-slide-up pb-20">
    <header className="text-center space-y-4">
      <h2 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-500">
        Analysis Complete
      </h2>
      <p className="text-slate-400">Here are your top career matches</p>
    </header>

    <div className="space-y-6">
      {results.length === 0 ? (
        <div className="text-center text-slate-500 py-12">No matches found. Try selecting more keywords.</div>
      ) : results.map((item, index) => (
        <div key={index} className="group relative bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-slate-500 transition-all overflow-hidden">
          <div className="absolute top-0 left-0 bottom-0 bg-gradient-to-r from-indigo-600/20 to-transparent transition-all duration-1000" style={{ width: `${item.score}%` }}></div>
          <div className="relative z-10 flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">{item.category}</div>
              <div className="text-2xl font-bold text-white group-hover:text-indigo-300 transition-colors">{item.post}</div>
              {item.breakdown && (
                <div className="mt-2 text-xs text-slate-400 space-y-1">
                  {item.breakdown.interests.length > 0 && (
                    <div><span className="text-pink-400 font-bold">♥</span> {item.breakdown.interests.join(', ')}</div>
                  )}
                  {item.breakdown.skills.length > 0 && (
                    <div><span className="text-indigo-400 font-bold">★</span> {item.breakdown.skills.join(', ')}</div>
                  )}
                </div>
              )}
            </div>
            <div className="flex flex-col items-end">
              <span className="text-4xl font-black text-white/90">{item.score}</span>
              <span className="text-xs text-slate-400 font-medium">MATCH SCORE</span>
            </div>
          </div>
        </div>
      ))}
    </div>

    <div className="text-center">
      <button
        onClick={onRestart}
        className="px-8 py-3 rounded-full border border-slate-600 text-slate-400 hover:text-white hover:border-white transition-all"
      >
        Try Again
      </button>
    </div>
  </div>
);

function App() {
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('home'); // home, select, result
  const [words, setWords] = useState({ like: [], cando: [] });
  const [choices, setChoices] = useState({ like: [], cando: [] });
  const [results, setResults] = useState([]);

  useEffect(() => {
    initModel().then(() => {
      // Artificial delay for smoother intro
      setTimeout(() => setLoading(false), 800);
    });
  }, []);

  const handleStart = () => {
    try {
      const w = generateWords();
      setWords(w);
      setChoices({ like: [], cando: [] });
      setView('select');
    } catch (e) {
      console.error(e);
      alert("Failed to generate words. Model might not be loaded.");
    }
  };

  const handleAnalyze = () => {
    const res = calcScore(choices);
    setResults(res);
    setView('result');
    window.scrollTo(0, 0);
  };

  if (loading) return <LoadingScreen />;

  return (
    <div className="min-h-screen font-sans">
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-800 via-slate-900 to-black -z-10"></div>
      <div className="container mx-auto px-4 py-8 md:py-16 min-h-screen">
        {view === 'home' && <Home onStart={handleStart} />}
        {view === 'select' && <Select words={words} choices={choices} setChoices={setChoices} onAnalyze={handleAnalyze} />}
        {view === 'result' && <Result results={results} onRestart={handleStart} />}
      </div>
    </div>
  );
}

export default App;
