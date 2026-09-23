import React, { useState, useEffect, useRef } from 'react';
import { 
  Upload, 
  Github, 
  ExternalLink, 
  Eye, 
  CheckCircle2, 
  ClipboardPaste,
  RefreshCw,
  Sparkles,
  BookOpen,
  ArrowRight,
  Copy,
  Download,
  Check,
  Shield,
  Lock,
  Key,
  FileText,
  X
} from 'lucide-react';

export default function App() {
  const [htmlContent, setHtmlContent] = useState<string>(() => {
    return localStorage.getItem('vrws_html_content') || '';
  });
  const [fileName, setFileName] = useState<string>(() => {
    return localStorage.getItem('vrws_file_name') || 'VRWS Opportunity Ledger (Pre-populated 94 Leads)';
  });
  const [password, setPassword] = useState('vrws2026');
  const [showSecurityModal, setShowSecurityModal] = useState(false);
  const [pastedCode, setPastedCode] = useState('');
  const [isPasting, setIsPasting] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [copied, setCopied] = useState(false);
  const [robotsCopied, setRobotsCopied] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load the complete 94-lead standalone file by default if none is stored
  useEffect(() => {
    if (!htmlContent) {
      fetch('/full-index.html')
        .then(res => res.text())
        .then(text => {
          if (text) {
            setHtmlContent(text);
            setFileName('VRWS 2026 Opportunity Ledger (94 leads)');
          }
        })
        .catch(err => console.error('Failed to load default full-index.html', err));
    }
  }, [htmlContent]);

  useEffect(() => {
    if (htmlContent) {
      localStorage.setItem('vrws_html_content', htmlContent);
      localStorage.setItem('vrws_file_name', fileName);
    }
  }, [htmlContent, fileName]);

  const getCleanHtml = () => {
    let cleaned = htmlContent;
    // Inject configured password
    cleaned = cleaned.replace(/const CONFIG_PASSWORD = "[^"]*";/g, `const CONFIG_PASSWORD = "${password}";`);
    // Remove Claude preamble if present
    cleaned = cleaned.replace(/<script>\s*window\.__FRAME_PREAMBLE[\s\S]*?<\/script>/gi, '');
    cleaned = cleaned.replace(/<script[^>]*preload-helper[^>]*>\s*<\/script>/gi, '');
    cleaned = cleaned.replace(/href=["']\.\/css2["']/gi, 'href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=Libre+Franklin:wght@700;800&display=swap"');
    return cleaned;
  };

  const handleCopyCode = async () => {
    const code = getCleanHtml();
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = code;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    }
  };

  const handleDownload = () => {
    const code = getCleanHtml();
    const blob = new Blob([code], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'index.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleCopyRobots = async () => {
    const robots = "User-agent: *\nDisallow: /\n";
    try {
      await navigator.clipboard.writeText(robots);
      setRobotsCopied(true);
      setTimeout(() => setRobotsCopied(false), 2500);
    } catch {
      setRobotsCopied(true);
      setTimeout(() => setRobotsCopied(false), 2500);
    }
  };

  const handleDownloadRobots = () => {
    const robots = "User-agent: *\nDisallow: /\n";
    const blob = new Blob([robots], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'robots.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleFile = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      if (content) {
        setHtmlContent(content);
        setFileName(file.name);
      }
    };
    reader.readAsText(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      handleFile(file);
    }
  };

  const handleApplyPasted = () => {
    if (pastedCode.trim()) {
      setHtmlContent(pastedCode.trim());
      setFileName('_t.html (Pasted Code)');
      setIsPasting(false);
    }
  };

  const handleReset = () => {
    setHtmlContent('');
    setFileName('');
    localStorage.removeItem('vrws_html_content');
    localStorage.removeItem('vrws_file_name');
    fetch('/full-index.html')
      .then(res => res.text())
      .then(text => {
        setHtmlContent(text);
        setFileName('VRWS 2026 Opportunity Ledger (94 leads)');
      });
  };

  if (htmlContent) {
    return (
      <div id="vrws-viewer-container" className="flex flex-col h-screen w-screen bg-slate-900 text-slate-100">
        <header id="vrws-viewer-header" className="h-14 border-b border-slate-700 bg-slate-800/95 px-4 flex items-center justify-between shrink-0 gap-3">
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center justify-center p-1.5 rounded-md bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <Eye className="w-4 h-4" />
            </span>
            <div>
              <h1 className="text-sm font-semibold tracking-tight text-white flex items-center gap-2">
                VRWS Opportunity Ledger
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  94 Leads Loaded
                </span>
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            <button
              id="security-settings-btn"
              onClick={() => setShowSecurityModal(true)}
              className="inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1.5 rounded-md bg-slate-700/80 hover:bg-slate-700 text-amber-300 border border-amber-500/30 transition-colors"
              title="Configure Password & Anti-Crawler Protection"
            >
              <Lock className="w-3.5 h-3.5 text-amber-400" />
              <span className="hidden sm:inline">Protection:</span>
              <span className="font-mono bg-slate-800 px-1 py-0.5 rounded text-[11px] text-white">
                {password}
              </span>
            </button>

            <button
              id="copy-html-btn"
              onClick={handleCopyCode}
              className={`inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-md transition-all shadow-sm ${
                copied 
                  ? 'bg-emerald-600 text-white' 
                  : 'bg-rose-600 hover:bg-rose-500 text-white'
              }`}
              title="Copy complete index.html for your GitHub repository"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copied to Clipboard!' : 'Copy Code for GitHub'}
            </button>

            <button
              id="download-html-btn"
              onClick={handleDownload}
              className="hidden sm:inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-md bg-slate-700 hover:bg-slate-600 text-slate-100 transition-colors"
              title="Download self-contained index.html file"
            >
              <Download className="w-3.5 h-3.5" />
              Download index.html
            </button>

            <a
              href="https://github.com/betobricio-blip/Sales-Dashboard-VRWS/edit/main/index.html"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 transition-colors"
            >
              <Github className="w-3.5 h-3.5" />
              <span className="hidden md:inline">Edit on GitHub</span>
              <ExternalLink className="w-3 h-3 text-slate-400" />
            </a>

            <button
              id="reload-file-btn"
              onClick={handleReset}
              className="inline-flex items-center gap-1 text-xs px-2 py-1.5 rounded-md text-slate-400 hover:text-slate-200 transition-colors"
              title="Reset or upload different file"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>
        </header>

        {/* Security / Protection Settings Modal */}
        {showSecurityModal && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
            <div className="bg-slate-900 border border-slate-700 rounded-xl p-5 max-w-md w-full shadow-2xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    <Shield className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white">Dashboard Access & Crawler Protection</h3>
                    <p className="text-[11px] text-slate-400">Settings for your GitHub Pages deployment</p>
                  </div>
                </div>
                <button
                  onClick={() => setShowSecurityModal(false)}
                  className="text-slate-400 hover:text-white p-1 rounded-md"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Password Setting */}
              <div className="space-y-2">
                <label className="block text-xs font-medium text-slate-300">
                  Access Passcode:
                </label>
                <div className="flex items-center gap-2">
                  <div className="relative flex-1">
                    <Key className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      value={password}
                      onChange={(e) => setPassword(e.target.value || 'vrws2026')}
                      className="w-full pl-9 pr-3 py-1.5 bg-slate-950 border border-slate-700 rounded-md text-xs font-mono text-white focus:outline-none focus:border-rose-500"
                      placeholder="e.g. vrws2026"
                    />
                  </div>
                  <span className="text-[11px] text-emerald-400 font-medium whitespace-nowrap">
                    Active
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Anyone accessing your GitHub URL will be prompted to type this password to view the leads.
                </p>
              </div>

              {/* Crawler Blocking Details */}
              <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3 space-y-2">
                <div className="flex items-center gap-2 text-xs font-medium text-slate-200">
                  <Shield className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Crawler & Search Engine Protection</span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  1. <strong className="text-slate-300">Meta Directives:</strong> <code className="text-rose-300 bg-slate-800 px-1 py-0.5 rounded">noindex, nofollow, noarchive</code> tags are embedded in the HTML to instruct Google, Bing, and AI bots not to index or display the page.
                  <br />
                  2. <strong className="text-slate-300">Data Concealment:</strong> The table contents are dynamically injected only upon successful password verification, so basic web scrapers receive zero company or contact data.
                </p>
              </div>

              {/* robots.txt helper */}
              <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs font-medium text-slate-200">
                    <FileText className="w-3.5 h-3.5 text-indigo-400" />
                    <span>robots.txt (Universal Crawler Block)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={handleCopyRobots}
                      className="text-[11px] px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                    >
                      {robotsCopied ? 'Copied!' : 'Copy'}
                    </button>
                    <button
                      onClick={handleDownloadRobots}
                      className="text-[11px] px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                    >
                      Download
                    </button>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400">
                  Add a file named <code className="text-rose-300">robots.txt</code> to your GitHub repo root to tell all search engines to stay away.
                </p>
              </div>

              <div className="pt-2 flex justify-end">
                <button
                  type="button"
                  onClick={() => setShowSecurityModal(false)}
                  className="px-4 py-1.5 text-xs font-medium bg-rose-600 hover:bg-rose-500 text-white rounded-md transition-colors"
                >
                  Done
                </button>
              </div>
            </div>
          </div>
        )}

        <main id="vrws-iframe-wrapper" className="flex-1 w-full bg-white relative">
          <iframe
            id="vrws-live-frame"
            title="VRWS Opportunity Ledger"
            srcDoc={htmlContent}
            sandbox="allow-scripts allow-same-origin allow-forms allow-modals allow-popups"
            className="w-full h-full border-0 absolute inset-0"
          />
        </main>
      </div>
    );
  }

  return (
    <div id="vrws-landing" className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-4 sm:p-6 font-sans">
      <div className="w-full max-w-2xl space-y-6">
        
        {/* Header Section */}
        <div id="vrws-intro" className="text-center space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs font-medium">
            <Sparkles className="w-3.5 h-3.5" />
            VRWS Opportunity Ledger Host
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
            VRWS Opportunity Ledger
          </h1>
          <p className="text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
            The HTML page saved from your browser is the outer Claude frame. The actual app content lives inside your companion folder in <span className="font-mono text-rose-300 bg-rose-950/40 px-1 py-0.5 rounded text-xs">_t.html</span>.
          </p>
        </div>

        {/* Action Card */}
        <div id="vrws-import-card" className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
          
          {/* Quick Preloaded 94 Leads action */}
          <div className="bg-rose-950/20 border border-rose-500/30 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-rose-200">
                Ready-to-Deploy 94 Leads Ledger
              </p>
              <p className="text-xs text-rose-300/80 mt-0.5">
                Complete dataset already compiled (56 Pipeline, 8 Potential, 9 Cold, 21 Customer)
              </p>
            </div>
            <div className="flex items-center gap-2 shrink-0 w-full sm:w-auto">
              <button
                type="button"
                onClick={() => {
                  fetch('/full-index.html')
                    .then(res => res.text())
                    .then(text => {
                      setHtmlContent(text);
                      setFileName('VRWS 2026 Opportunity Ledger (94 leads)');
                    });
                }}
                className="flex-1 sm:flex-none px-3.5 py-1.5 text-xs font-medium rounded-md bg-rose-600 hover:bg-rose-500 text-white transition-colors"
              >
                Open Ledger
              </button>
            </div>
          </div>

          {/* Drag and drop zone */}
          <div
            id="dropzone"
            onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-3 ${
              isDragOver 
                ? 'border-rose-500 bg-rose-500/5' 
                : 'border-slate-700 hover:border-slate-600 bg-slate-950/50 hover:bg-slate-950/80'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".html,.htm"
              className="hidden"
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  handleFile(e.target.files[0]);
                }
              }}
            />
            <div className="p-3 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <Upload className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-200">
                Drop <span className="text-rose-400 font-mono">_t.html</span> here or click to browse
              </p>
              <p className="text-xs text-slate-500 mt-1">
                Located inside your <span className="font-mono">VRWS Opportunity Ledger_files</span> folder
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="h-px bg-slate-800 flex-1" />
            <span className="text-xs uppercase text-slate-500 font-semibold tracking-wider">or</span>
            <div className="h-px bg-slate-800 flex-1" />
          </div>

          {/* Paste code toggle */}
          <div>
            {!isPasting ? (
              <button
                id="toggle-paste-btn"
                type="button"
                onClick={() => setIsPasting(true)}
                className="w-full py-2.5 px-4 rounded-lg bg-slate-800 hover:bg-slate-750 border border-slate-700 text-slate-200 text-xs font-medium flex items-center justify-center gap-2 transition-colors"
              >
                <ClipboardPaste className="w-4 h-4 text-slate-400" />
                Paste code from _t.html directly
              </button>
            ) : (
              <div className="space-y-3">
                <label htmlFor="pasted-textarea" className="block text-xs font-medium text-slate-300">
                  Open <span className="font-mono text-rose-300">_t.html</span> in Notepad / TextEdit, copy all, and paste below:
                </label>
                <textarea
                  id="pasted-textarea"
                  rows={6}
                  value={pastedCode}
                  onChange={(e) => setPastedCode(e.target.value)}
                  placeholder="<!DOCTYPE html><html>... Paste the code from _t.html here ..."
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs font-mono text-slate-300 placeholder:text-slate-600 focus:outline-none focus:border-rose-500"
                />
                <div className="flex items-center justify-end gap-2">
                  <button
                    type="button"
                    onClick={() => setIsPasting(false)}
                    className="px-3 py-1.5 text-xs text-slate-400 hover:text-slate-200"
                  >
                    Cancel
                  </button>
                  <button
                    id="apply-pasted-btn"
                    type="button"
                    onClick={handleApplyPasted}
                    disabled={!pastedCode.trim()}
                    className="px-4 py-1.5 text-xs font-medium bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white rounded-md transition-colors"
                  >
                    View HTML
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Step-by-Step GitHub Pages Guide */}
        <div id="github-hosting-instructions" className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4 text-xs">
          <div className="flex items-center gap-2 text-white font-semibold text-sm">
            <Github className="w-4 h-4 text-slate-200" />
            <h2>How to Make Your HTML Visible to Others on GitHub (Step-by-Step)</h2>
          </div>

          <p className="text-slate-400 leading-relaxed">
            To publish your saved web page on GitHub so that anyone with a link can open and see it, use <strong>GitHub Pages</strong> (GitHub&apos;s free website hosting):
          </p>

          <ol className="space-y-3 text-slate-300 list-decimal list-inside">
            <li className="space-y-1">
              <strong className="text-white">Create a GitHub Repository:</strong>
              <p className="text-slate-400 pl-4">
                Go to <a href="https://github.com/new" target="_blank" rel="noreferrer" className="text-rose-400 underline inline-flex items-center gap-0.5">github.com/new <ExternalLink className="w-2.5 h-2.5" /></a>, name it <code className="bg-slate-800 px-1 py-0.5 rounded text-rose-300">vrws-ledger</code>, set it to <strong>Public</strong>, and click <strong>Create repository</strong>.
              </p>
            </li>

            <li className="space-y-1">
              <strong className="text-white">Upload Both the HTML File AND the Folder:</strong>
              <p className="text-slate-400 pl-4">
                Click <strong>&ldquo;Add file&rdquo; &gt; &ldquo;Upload files&rdquo;</strong> in your GitHub repository. Drag both your <code className="bg-slate-800 px-1 py-0.5 rounded text-rose-300">index.html</code> (or rename it to <code className="bg-slate-800 px-1 py-0.5 rounded text-rose-300">index.html</code>) and the companion folder <code className="bg-slate-800 px-1 py-0.5 rounded text-rose-300">VRWS Opportunity Ledger_files</code> together into GitHub. Click <strong>Commit changes</strong>.
              </p>
            </li>

            <li className="space-y-1">
              <strong className="text-white">Activate GitHub Pages:</strong>
              <p className="text-slate-400 pl-4">
                In your repository, click <strong>Settings</strong> (top tab) &gt; click <strong>Pages</strong> in the left sidebar &gt; under <strong>Branch</strong>, select <code className="bg-slate-800 px-1 py-0.5 rounded text-white">main</code> (or <code className="bg-slate-800 px-1 py-0.5 rounded text-white">master</code>) &gt; click <strong>Save</strong>.
              </p>
            </li>

            <li className="space-y-1">
              <strong className="text-white">Your Public Link is Ready:</strong>
              <p className="text-slate-400 pl-4">
                In 1–2 minutes, GitHub will display your live public link (e.g. <code className="bg-slate-800 px-1 py-0.5 rounded text-emerald-400">https://yourusername.github.io/vrws-ledger/</code>) that anyone can visit!
              </p>
            </li>
          </ol>
        </div>

      </div>
    </div>
  );
}
