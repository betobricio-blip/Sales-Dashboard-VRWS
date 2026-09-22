import React, { useState, useEffect, useRef } from 'react';
import { 
  Upload, 
  FileCode, 
  FolderArchive, 
  Github, 
  ExternalLink, 
  Eye, 
  CheckCircle2, 
  AlertTriangle, 
  ClipboardPaste,
  RefreshCw,
  Sparkles
} from 'lucide-react';

export default function App() {
  const [htmlContent, setHtmlContent] = useState<string>(() => {
    return localStorage.getItem('vrws_html_content') || '';
  });
  const [fileName, setFileName] = useState<string>(() => {
    return localStorage.getItem('vrws_file_name') || '';
  });
  const [pastedCode, setPastedCode] = useState('');
  const [isPasting, setIsPasting] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (htmlContent) {
      localStorage.setItem('vrws_html_content', htmlContent);
      localStorage.setItem('vrws_file_name', fileName);
    }
  }, [htmlContent, fileName]);

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
      setFileName('_t.html (Pasted Content)');
      setIsPasting(false);
    }
  };

  const handleReset = () => {
    setHtmlContent('');
    setFileName('');
    localStorage.removeItem('vrws_html_content');
    localStorage.removeItem('vrws_file_name');
  };

  if (htmlContent) {
    return (
      <div id="vrws-viewer-container" className="flex flex-col h-screen w-screen bg-slate-900 text-slate-100">
        <header id="vrws-viewer-header" className="h-12 border-b border-slate-700 bg-slate-800/90 px-4 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center justify-center p-1.5 rounded-md bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <Eye className="w-4 h-4" />
            </span>
            <div>
              <h1 className="text-sm font-semibold tracking-tight text-white flex items-center gap-2">
                VRWS Opportunity Ledger
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  Live Preview
                </span>
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 truncate max-w-xs hidden sm:inline">
              Source: {fileName}
            </span>
            <button
              id="reload-file-btn"
              onClick={handleReset}
              className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Upload Different File
            </button>
          </div>
        </header>

        <main id="vrws-iframe-wrapper" className="flex-1 w-full bg-white relative">
          <iframe
            id="vrws-live-frame"
            title="VRWS Opportunity Ledger App"
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
            Claude Artifact Importer
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
            VRWS Opportunity Ledger
          </h1>
          <p className="text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
            The HTML page you copied is Claude&apos;s outer window wrapper. The interactive application itself is stored inside your companion folder in <span className="font-mono text-rose-300 bg-rose-950/40 px-1 py-0.5 rounded text-xs">_t.html</span>.
          </p>
        </div>

        {/* Action Card */}
        <div id="vrws-import-card" className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
          
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
                Drop <span className="text-rose-400 font-mono">_t.html</span> here or browse
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
                    Launch VRWS Ledger
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* GitHub & Online Access Instructions */}
        <div id="vrws-guide" className="bg-slate-900/50 border border-slate-800/80 rounded-xl p-5 space-y-4 text-xs text-slate-300">
          <h2 className="font-semibold text-slate-100 flex items-center gap-2">
            <Github className="w-4 h-4 text-slate-300" />
            Viewing Online & Exporting to GitHub
          </h2>
          <div className="grid sm:grid-cols-2 gap-3 text-slate-400">
            <div className="space-y-1">
              <span className="font-medium text-slate-200 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                See It Online Immediately
              </span>
              <p>
                Google AI Studio hosts this app live at your application URL. Click <strong>Share</strong> in the top header or open in a new tab.
              </p>
            </div>
            <div className="space-y-1">
              <span className="font-medium text-slate-200 flex items-center gap-1.5">
                <ExternalLink className="w-3.5 h-3.5 text-rose-400" />
                Upload to GitHub
              </span>
              <p>
                Open the <strong>Settings</strong> or menu at the top of Google AI Studio, choose <strong>Export to GitHub</strong>, and connect your repository in one click.
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

