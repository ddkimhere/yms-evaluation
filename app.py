<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YMS 월말평가 인쇄 및 편집 관리 시스템</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Inter:wght=300;400;500;600;700;800&family=Noto+Sans+KR:wght=300;400;500;700;900&family=Nanum+Myeongjo:wght=400;700;800&display=swap');
        
        body {
            font-family: 'Noto Sans KR', 'Inter', sans-serif;
        }

        /* Realistic A4 Paper Live Preview styling for Screen */
        .paper-preview {
            background-color: white;
            box-shadow: 0 15px 35px rgba(15, 23, 42, 0.08);
            color: #111827;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }

        /* Custom handwriting dotted lines for paper translations */
        .writing-line {
            border-bottom: 1px dotted #475569;
            height: 2.3rem;
            margin-top: 0.4rem;
            position: relative;
        }
        
        /* Teacher Answer view coloring */
        .teacher-answer {
            color: #dc2626 !important;
            font-weight: bold;
            font-family: 'Nanum Myeongjo', serif;
        }

        /* Scrollbar custom style */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }

        /* Junior Mode Custom Design Override */
        .junior-mode {
            font-size: 13.5px !important;
        }
        .junior-mode h2 {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 24px !important;
            font-weight: 800 !important;
        }
        .junior-mode p {
            font-size: 13px !important;
            line-height: 1.8 !important;
        }
        .junior-mode .writing-line {
            height: 2.8rem !important;
            border-bottom: 2px dashed #94a3b8 !important;
            margin-top: 0.8rem !important;
        }

        /* Print media styles */
        @media print {
            body {
                background: white !important;
                color: black !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            .no-print {
                display: none !important;
            }
            .paper-preview {
                box-shadow: none !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
                width: 100% !important;
                max-width: 100% !important;
            }
            .print-page-break {
                page-break-before: always !important;
                break-before: page !important;
                height: 0 !important;
                margin: 0 !important;
                border: none !important;
            }
            .avoid-break {
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
            .writing-line {
                border-bottom: 1px dotted #334155 !important;
            }
            .junior-mode .writing-line {
                border-bottom: 2px dashed #334155 !important;
            }
            .page-break-indicator {
                display: none !important;
            }
            * {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
        }
    </style>
</head>
<body class="bg-slate-100 min-h-screen text-slate-800 pb-16 transition-colors duration-300">

    <!-- AI Generation Loading Modal Overlay -->
    <div id="ai-loading-overlay" class="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-[200] flex flex-col items-center justify-center hidden">
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl max-w-md w-full mx-4 shadow-2xl flex flex-col items-center space-y-5 text-center">
            <div class="relative">
                <div class="w-16 h-16 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin"></div>
                <i class="fa-solid fa-wand-magic-sparkles text-xl text-indigo-400 absolute inset-0 m-auto w-fit h-fit animate-bounce"></i>
            </div>
            <div class="space-y-2">
                <h3 class="text-white font-bold text-lg flex items-center justify-center gap-2">
                    <span>Gemini AI 시험지 마법 발동 중</span>
                </h3>
                <p id="ai-loading-step" class="text-xs text-indigo-300 font-semibold animate-pulse">선택된 수준의 고품질 문제를 출제하는 중...</p>
                <p class="text-[10px] text-slate-500 leading-relaxed">구글의 초거대 AI가 실시간으로 가장 최적화된 명품 독해 지문과 고품질 평가 문항 데이터를 결합하여 빌드 중입니다.</p>
            </div>
        </div>
    </div>

    <!-- Top Configuration & Navigation Bar -->
    <header class="no-print bg-slate-900 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="bg-indigo-600 p-2 rounded-lg text-white">
                    <i class="fa-solid fa-graduation-cap text-xl"></i>
                </div>
                <div>
                    <h1 class="text-md font-bold tracking-tight flex items-center gap-2">
                        <span>YMS 영어 학업성취도 평가 인쇄 시스템</span>
                        <span class="text-[10px] bg-indigo-500 text-white font-semibold px-2 py-0.5 rounded-full">AI 마스터 v5.0</span>
                    </h1>
                    <p id="header-summary" class="text-[11px] text-slate-400">지정된 문항 수에 맞게 실시간 배점이 조정됩니다.</p>
                </div>
            </div>

            <div class="flex flex-wrap items-center gap-3">
                <button onclick="generateAIQuestionsAllPassages()" class="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold px-3 py-2 rounded-lg text-xs transition flex items-center gap-1.5 shadow-md">
                    <i class="fa-solid fa-wand-magic-sparkles text-amber-300 animate-pulse"></i>
                    <span>🪄 전체 지문 기반 AI 문제 일괄 생성</span>
                </button>
                <button onclick="toggleTeacherDrawer()" id="btn-teacher-toggle" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold px-3 py-2 rounded-lg text-xs transition flex items-center gap-1.5">
                    <i class="fa-solid fa-sliders text-amber-400"></i>
                    <span>선생님 문제 편집기</span>
                </button>
                <button onclick="triggerPrint()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-lg text-xs transition flex items-center gap-1.5 shadow-md">
                    <i class="fa-solid fa-print"></i> PDF 다운로드 / 인쇄
                </button>
            </div>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-4 mt-6">
        
        <!-- Teacher Dashboard Drawer -->
        <div id="teacher-drawer" class="no-print hidden mb-6 bg-slate-900 text-slate-100 rounded-xl p-5 border border-slate-800 shadow-2xl space-y-4">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h2 class="text-sm font-bold flex items-center gap-2 text-amber-400">
                    <i class="fa-solid fa-gears"></i> 실시간 시험 문제 빌더 & 문항수 맞춤 관리 도구
                </h2>
            </div>
            
            <!-- Quick Paper Metadata Settings -->
            <div class="grid grid-cols-2 md:grid-cols-8 gap-3 text-xs">
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">대상 학년 레벨</label>
                    <select id="config-level" onchange="changeLevel(this.value)" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white focus:outline-none focus:border-indigo-500 font-bold text-amber-400">
                        <option value="elementary_junior">초등 저학년 (2~4학년)</option>
                        <option value="elementary">초등 고학년 (5~6학년)</option>
                        <option value="middle" selected>중등부 (Middle)</option>
                    </select>
                </div>
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">단어 문항수</label>
                    <input type="number" id="config-vocab-count" value="20" min="5" max="30" step="5" oninput="changeVocabCount(this.value)" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white font-bold">
                </div>
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">단어 출제방식</label>
                    <select id="config-vocab-type" onchange="changeVocabType(this.value)" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white font-bold text-amber-400">
                        <option value="mean">뜻 적기</option>
                        <option value="eng">영어 적기</option>
                        <option value="mixed">뜻,영어 같이</option>
                        <option value="matching" selected>그림-단어 선 잇기</option>
                    </select>
                </div>
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">독해 지문수</label>
                    <input type="number" id="config-reading-count" value="5" min="1" max="5" oninput="changeReadingCount(this.value)" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white font-bold">
                </div>
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">영한해석 문항수</label>
                    <input type="number" id="config-translation-count" value="10" min="5" max="15" oninput="changeTranslationCount(this.value)" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white font-bold">
                </div>
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">어순배열 문항수</label>
                    <input type="number" id="config-unscramble-count" value="10" min="5" max="15" oninput="changeUnscrambleCount(this.value)" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white font-bold">
                </div>
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">학원명</label>
                    <input type="text" id="config-academy" value="YMS 어학원" oninput="syncHeaderData()" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white">
                </div>
                <div class="md:col-span-1">
                    <label class="block text-slate-400 font-medium mb-1">과목명</label>
                    <input type="text" id="config-subject" value="영어 (English)" oninput="syncHeaderData()" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white">
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                <div>
                    <label class="block text-slate-400 font-medium mb-1">시험지 대제목</label>
                    <input type="text" id="config-title" value="Premium Monthly Evaluation" oninput="syncHeaderData()" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white">
                </div>
                <div>
                    <label class="block text-slate-400 font-medium mb-1">인쇄 일자</label>
                    <input type="text" id="config-date" value="2026. 06" oninput="syncHeaderData()" class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white">
                </div>
                <div>
                    <label class="block text-slate-400 font-medium mb-1 flex items-center justify-between">
                        <span class="text-indigo-400 font-bold"><i class="fa-solid fa-key mr-1 text-amber-400"></i> Gemini API Key 설정</span>
                        <a href="https://aistudio.google.com/" target="_blank" class="text-[10px] text-slate-400 hover:text-indigo-400 transition">무료 발급받기</a>
                    </label>
                    <input type="password" id="config-api-key" oninput="saveApiKey(this.value)" placeholder="AI Studio의 API Key를 입력하세요..." class="w-full bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-white text-[11px] font-mono">
                </div>
            </div>

            <!-- Tab Controls for Bulk Editors -->
            <div class="border-t border-slate-800 pt-3">
                <div class="flex gap-1.5 border-b border-slate-800 mb-3" id="editor-tabs">
                    <button onclick="switchEditorTab('vocab')" id="tab-vocab" class="px-3 py-1.5 text-xs font-semibold text-white border-b-2 border-indigo-500 bg-slate-800 rounded-t-md">단어</button>
                    <button onclick="switchEditorTab('reading')" id="tab-reading" class="px-3 py-1.5 text-xs font-semibold text-slate-400 hover:text-white rounded-t-md">독해 지문 및 AI 문항</button>
                    <button onclick="switchEditorTab('translation')" id="tab-translation" class="px-3 py-1.5 text-xs font-semibold text-slate-400 hover:text-white rounded-t-md">영한해석</button>
                    <button onclick="switchEditorTab('unscramble')" id="tab-unscramble" class="px-3 py-1.5 text-xs font-semibold text-slate-400 hover:text-white rounded-t-md">어순배열</button>
                </div>

                <!-- Vocab Editor Panel -->
                <div id="panel-vocab" class="editor-panel space-y-2">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                        <div>
                            <label class="block text-[11px] text-slate-300 font-bold mb-1">영어 단어 목록 (줄바꿈 구분)</label>
                            <textarea id="edit-vocab-eng" rows="6" onpaste="handleVocabEngPaste(event)" placeholder="영어 단어를 입력하세요." class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 font-mono text-xs text-emerald-400 focus:outline-none"></textarea>
                        </div>
                        <div>
                            <label class="block text-[11px] text-slate-300 font-bold mb-1">한글 뜻 목록 (줄바꿈 구분)</label>
                            <textarea id="edit-vocab-kor" rows="6" placeholder="한글 뜻을 입력하세요." class="w-full bg-slate-955 border border-slate-800 rounded-lg p-2.5 font-mono text-xs text-emerald-400 focus:outline-none"></textarea>
                        </div>
                    </div>
                    <div class="flex justify-end pt-1">
                        <button onclick="applyVocabChange()" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-1.5 rounded transition">단어 데이터 반영</button>
                    </div>
                </div>

                <!-- Reading Editor Panel -->
                <div id="panel-reading" class="editor-panel hidden space-y-4">
                    <div id="reading-editor-list" class="space-y-4 max-h-96 overflow-y-auto pr-2"></div>
                    <div class="flex justify-end pt-2 border-t border-slate-800">
                        <button onclick="applyReadingChange()" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-1.5 rounded transition">독해 지문 전체 적용</button>
                    </div>
                </div>

                <!-- Translation Editor Panel -->
                <div id="panel-translation" class="editor-panel hidden space-y-2">
                    <p class="text-xs text-slate-400">한 줄에 하나씩 <strong class="text-indigo-400">영어문장=한국어해석</strong> 형식으로 기입하세요.</p>
                    <textarea id="edit-translation" rows="6" placeholder="Example Sentence=예시 한국어 번역문" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 font-mono text-xs text-emerald-400 focus:outline-none leading-relaxed"></textarea>
                    <div class="flex justify-end pt-1">
                        <button onclick="applyTranslationChange()" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-1.5 rounded transition">영한해석 데이터 반영</button>
                    </div>
                </div>

                <!-- Unscramble Editor Panel -->
                <div id="panel-unscramble" class="editor-panel hidden space-y-2">
                    <p class="text-xs text-slate-400">한 줄에 하나씩 <strong class="text-indigo-400">영어완성문장=한국어힌트</strong> 형식으로 기입하세요.</p>
                    <textarea id="edit-unscramble" rows="6" placeholder="I have a book=나는 책을 가지고 있다" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 font-mono text-xs text-emerald-400 focus:outline-none leading-relaxed"></textarea>
                    <div class="flex justify-end pt-1">
                        <button onclick="applyUnscrambleChange()" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-1.5 rounded transition">어순배열 데이터 반영</button>
                    </div>
                </div>
            </div>

            <!-- Global Action Tools -->
            <div class="flex justify-between items-center pt-3 border-t border-slate-800 text-xs font-semibold">
                <span class="text-amber-500"><i class="fa-solid fa-triangle-exclamation"></i> 주의: 캐시 소실 방지를 위해 수시로 보관하기를 누르세요.</span>
                <div class="flex gap-2">
                    <button onclick="saveToLocalStorage()" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 px-3 py-1.5 rounded-lg transition"><i class="fa-solid fa-floppy-disk mr-1"></i> 변경안 캐시 보관</button>
                    <button onclick="resetToDemo()" class="bg-rose-950/40 hover:bg-rose-950 text-rose-300 border border-rose-900/50 px-3 py-1.5 rounded-lg transition">기본 데모 세트 복원</button>
                </div>
            </div>
        </div>

        <!-- VIEW: PAPER PRINT PREVIEW MODE -->
        <div id="view-paper-preview" class="flex flex-col lg:flex-row gap-6 justify-center">
            
            <!-- Left Side Control Column -->
            <div class="lg:w-80 space-y-4 no-print flex-shrink-0">
                <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-sm space-y-4 sticky top-24">
                    
                    <div class="bg-gradient-to-r from-purple-500 to-indigo-600 p-4 rounded-xl text-white space-y-2.5 shadow-md">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-amber-300 text-sm animate-bounce"></i>
                            <h4 class="text-xs font-extrabold tracking-wide">Gemini AI 일괄 출제</h4>
                        </div>
                        <p class="text-[10px] text-purple-100 leading-relaxed">선생님이 지문을 먼저 다 입력한 뒤, 이 버튼을 누르면 AI가 모든 지문을 분석해 일괄 출제합니다.</p>
                        <button onclick="generateAIQuestionsAllPassages()" class="w-full bg-white text-indigo-700 font-extrabold text-[11px] py-2 rounded-lg hover:bg-indigo-50 transition shadow">
                            전체 지문 AI 일괄 출제 시작
                        </button>
                    </div>

                    <h3 class="text-xs font-extrabold text-slate-900 pb-2 border-b flex items-center justify-between">
                        <span>인쇄용 퀵 설정 바</span>
                        <i class="fa-solid fa-print text-indigo-600"></i>
                    </h3>
                    
                    <div class="space-y-3 bg-slate-50 p-3 rounded-lg border border-slate-200">
                        <div class="space-y-1">
                            <label class="block text-[10px] text-slate-500 font-bold">평가 대상 학년</label>
                            <div class="grid grid-cols-3 gap-1">
                                <button onclick="changeLevel('elementary_junior')" id="sidebar-btn-elem-jr" class="py-1 px-1 bg-white text-slate-700 border rounded font-semibold text-[10px] transition truncate">초등 저(2-4)</button>
                                <button onclick="changeLevel('elementary')" id="sidebar-btn-elem" class="py-1 px-1 bg-white text-slate-700 border rounded font-semibold text-[10px] transition truncate">초등 고(5-6)</button>
                                <button onclick="changeLevel('middle')" id="sidebar-btn-mid" class="py-1 px-1 bg-white text-slate-700 border rounded font-semibold text-[10px] transition truncate">중등부</button>
                            </div>
                        </div>
                        
                        <div class="space-y-1">
                            <label class="block text-[10px] text-slate-500 font-bold">단어 문항 수</label>
                            <div class="flex items-center gap-2">
                                <input type="range" id="sidebar-range-vocab" min="5" max="30" step="5" value="20" oninput="changeVocabCount(this.value)" class="w-full accent-indigo-600">
                                <span id="sidebar-val-vocab" class="text-xs font-bold text-indigo-600 w-8 text-right">20개</span>
                            </div>
                        </div>

                        <div class="space-y-1">
                            <label class="block text-[10px] text-slate-500 font-bold">단어 출제 방식</label>
                            <select id="sidebar-vocab-type" onchange="changeVocabType(this.value)" class="w-full bg-white border rounded p-1.5 text-xs font-semibold text-slate-700">
                                <option value="mean">뜻 적기 (영어 → 한글)</option>
                                <option value="eng">영어 적기 (한글 → 영어)</option>
                                <option value="mixed">뜻, 영어 같이 (혼합)</option>
                                <option value="matching" selected>그림-단어 선 잇기 (Matching)</option>
                            </select>
                        </div>

                        <div class="space-y-1">
                            <label class="block text-[10px] text-slate-500 font-bold">독해 지문 수</label>
                            <div class="flex items-center gap-2">
                                <input type="range" id="sidebar-range-reading" min="1" max="5" step="1" value="5" oninput="changeReadingCount(this.value)" class="w-full accent-indigo-600">
                                <span id="sidebar-val-reading" class="text-xs font-bold text-indigo-600 w-8 text-right">5개</span>
                            </div>
                        </div>

                        <div class="space-y-1">
                            <label class="block text-[10px] text-slate-500 font-bold">영한해석 문항 수</label>
                            <div class="flex items-center gap-2">
                                <input type="range" id="sidebar-range-translation" min="5" max="15" step="1" value="10" oninput="changeTranslationCount(this.value)" class="w-full accent-indigo-600">
                                <span id="sidebar-val-translation" class="text-xs font-bold text-indigo-600 w-8 text-right">10개</span>
                            </div>
                        </div>

                        <div class="space-y-1">
                            <label class="block text-[10px] text-slate-500 font-bold">어순배열 문항 수</label>
                            <div class="flex items-center gap-2">
                                <input type="range" id="sidebar-range-unscramble" min="5" max="15" step="1" value="10" oninput="changeUnscrambleCount(this.value)" class="w-full accent-indigo-600">
                                <span id="sidebar-val-unscramble" class="text-xs font-bold text-indigo-600 w-8 text-right">10개</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="space-y-1.5">
                        <label class="block text-[10px] text-slate-500 font-bold">시험지 출력 모드</label>
                        <div class="grid grid-cols-2 gap-1.5">
                            <button onclick="togglePaperAnswerView(false)" id="paper-btn-student" class="py-1.5 bg-indigo-600 text-white font-bold text-xs rounded transition shadow">학생용 시험지</button>
                            <button onclick="togglePaperAnswerView(true)" id="paper-btn-teacher" class="py-1.5 bg-slate-100 text-slate-700 font-semibold text-xs rounded transition">교사용 정답지</button>
                        </div>
                    </div>

                    <div class="space-y-2 pt-2 border-t text-[11px] text-slate-600">
                        <div class="flex items-center gap-2 font-bold text-slate-800">
                            <i class="fa-solid fa-scissors text-amber-500 text-xs"></i>
                            <span>인쇄 페이지 수동 조절</span>
                        </div>
                        <div class="space-y-1.5 pl-0.5">
                            <button onclick="togglePageBreak('break-reading')" id="btn-break-reading" class="w-full text-left bg-slate-50 p-2 rounded border text-[10px] font-medium flex justify-between items-center transition">
                                <span>[II] 독해 시작점 분리</span><i class="fa-solid fa-plus-circle text-slate-400"></i>
                            </button>
                            <button onclick="togglePageBreak('break-translation')" id="btn-break-translation" class="w-full text-left bg-slate-50 p-2 rounded border text-[10px] font-medium flex justify-between items-center transition">
                                <span>[III] 해석 시작점 분리</span><i class="fa-solid fa-plus-circle text-slate-400"></i>
                            </button>
                            <button onclick="togglePageBreak('break-unscramble')" id="btn-break-unscramble" class="w-full text-left bg-slate-50 p-2 rounded border text-[10px] font-medium flex justify-between items-center transition">
                                <span>[IV] 배열 시작점 분리</span><i class="fa-solid fa-plus-circle text-slate-400"></i>
                            </button>
                        </div>
                    </div>

                    <div class="pt-2 border-t">
                        <button onclick="triggerPrint()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold py-2.5 rounded-lg transition flex items-center justify-center gap-1.5 shadow-md">
                            <i class="fa-solid fa-print"></i> PDF 다운로드 / 인쇄
                        </button>
                    </div>
                </div>
            </div>

            <!-- Realistic Printable A4 Sheet Render Frame -->
            <div id="print-sheet" class="paper-preview w-full max-w-[210mm] min-h-[297mm] p-8 md:p-12 relative bg-white transition-all duration-300">
                
                <!-- RE-DESIGNED SOPHISTICATED PRINT HEADER -->
                <div class="relative pb-3 mb-5 border-b-2 border-slate-900">
                    <div class="absolute top-0 left-0 w-full h-[3px] bg-slate-900"></div>
                    <div class="pt-3">
                        <!-- 1번 수정 반영: YMS 어학원 텍스트 완벽 제거 -->
                        <span class="text-sm font-black tracking-tight text-slate-900 block font-sans">YMS ENGLISH</span>
                    </div>
                    
                    <!-- 2번 수정 반영: 타이틀 마진(my-6 -> my-3)을 줄여 YMS ENGLISH와의 간격을 긴밀하게 압축 -->
                    <h2 id="paper-title-display" class="text-center font-extrabold text-2xl tracking-tight my-3 text-slate-900 font-serif">
                        Premium Monthly Evaluation
                    </h2>
                    
                    <div class="flex justify-between items-center bg-slate-50 border border-slate-200 rounded-lg p-2 text-[11px] font-medium font-sans mt-4">
                        <div class="w-1/3 text-left pl-2 text-slate-700 font-bold">
                            시험 날짜: <span id="paper-date-display" class="font-bold font-mono">2026. 06</span>
                        </div>
                        <div class="w-2/3 text-right flex justify-end items-center gap-2 text-slate-700">
                            <span>과목: <span id="paper-subject-display" class="font-semibold mr-3">영어</span></span>
                            <span>Class: <span class="border-b border-slate-400 w-16 inline-block mr-3">&nbsp;</span></span>
                            <span>성명(Name): <span class="border-b border-slate-400 w-24 inline-block">&nbsp;</span></span>
                        </div>
                    </div>
                </div>

                <!-- DYNAMIC EXAM SECTIONS -->
                <div class="space-y-6" id="paper-content-area">
                    
                    <!-- Section 1: Vocabulary -->
                    <div class="avoid-break">
                        <h3 class="font-bold text-xs bg-slate-100 px-2 py-1.5 border-l-4 border-slate-900 mb-3 flex justify-between items-center">
                            <div class="flex flex-col">
                                <span id="paper-vocab-title-display" class="font-bold"></span>
                                <span id="paper-vocab-score-display" class="text-[9px] font-normal text-slate-500"></span>
                            </div>
                            <div class="flex items-center gap-1 text-rose-600 font-bold border border-rose-300 px-1.5 py-0.5 rounded bg-rose-50/50 text-[10px]">
                                <span>득점:</span><span class="border-b border-rose-400 w-7 inline-block text-center">&nbsp;</span><span>/ 100</span>
                            </div>
                        </h3>
                        <p id="paper-vocab-instruction-display" class="text-[11px] text-slate-600 mb-3 font-serif"></p>
                        <div id="paper-vocab-grid" class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-[11px] font-serif"></div>
                        <div id="paper-vocab-matching-container" class="hidden space-y-6"></div>
                    </div>

                    <div id="break-reading"></div>

                    <!-- Section 2: Reading Comprehension -->
                    <div>
                        <h3 class="font-bold text-xs bg-slate-100 px-2 py-1.5 border-l-4 border-slate-900 mb-3 flex justify-between items-center">
                            <div class="flex flex-col">
                                <span id="paper-reading-title-display" class="font-bold"></span>
                                <span id="paper-reading-score-display" class="text-[9px] font-normal text-slate-500"></span>
                            </div>
                            <div class="flex items-center gap-1 text-rose-600 font-bold border border-rose-300 px-1.5 py-0.5 rounded bg-rose-50/50 text-[10px]">
                                <span>득점:</span><span class="border-b border-rose-400 w-7 inline-block text-center">&nbsp;</span><span>/ 100</span>
                            </div>
                        </h3>
                        <p class="text-[11px] text-slate-600 mb-3 font-serif">※ 다음 독해 문항들을 정독하고 질문에 가장 올바른 답을 기입하시오.</p>
                        <div id="paper-reading-list" class="space-y-6"></div>
                    </div>

                    <div id="break-translation"></div>

                    <!-- Section 3: Translation -->
                    <div>
                        <h3 class="font-bold text-xs bg-slate-100 px-2 py-1.5 border-l-4 border-slate-900 mb-3 flex justify-between items-center">
                            <div class="flex flex-col">
                                <span id="paper-translation-title-display" class="font-bold"></span>
                                <span id="paper-translation-score-display" class="text-[9px] font-normal text-slate-500"></span>
                            </div>
                            <div class="flex items-center gap-1 text-rose-600 font-bold border border-rose-300 px-1.5 py-0.5 rounded bg-rose-50/50 text-[10px]">
                                <span>득점:</span><span class="border-b border-rose-400 w-7 inline-block text-center">&nbsp;</span><span>/ 100</span>
                            </div>
                        </h3>
                        <p class="text-[11px] text-slate-600 mb-3 font-serif">※ 다음 영어 원문을 문맥에 맞게 매끄러운 한글 한국어 번역문으로 서술하시오.</p>
                        <div id="paper-translation-list" class="space-y-4 text-[11px] font-serif"></div>
                    </div>

                    <div id="break-unscramble"></div>

                    <!-- Section 4: Unscramble -->
                    <div>
                        <h3 class="font-bold text-xs bg-slate-100 px-2 py-1.5 border-l-4 border-slate-900 mb-3 flex justify-between items-center">
                            <div class="flex flex-col">
                                <span id="paper-unscramble-title-display" class="font-bold"></span>
                                <span id="paper-unscramble-score-display" class="text-[9px] font-normal text-slate-500"></span>
                            </div>
                            <div class="flex items-center gap-1 text-rose-600 font-bold border border-rose-300 px-1.5 py-0.5 rounded bg-rose-50/50 text-[10px]">
                                <span>득점:</span><span class="border-b border-rose-400 w-7 inline-block text-center">&nbsp;</span><span>/ 100</span>
                            </div>
                        </h3>
                        <p class="text-[11px] text-slate-600 mb-3 font-serif">※ 주어진 한글 뜻 힌트를 기반으로 박스 안의 영단어 카드를 바르게 어순 배열하시오.</p>
                        <div id="paper-unscramble-list" class="space-y-4 text-[11px] font-serif"></div>
                    </div>
                </div>

                <div class="border-t border-slate-400 text-center text-[9px] text-slate-500 mt-10 pt-4 font-serif">
                    본 평가 문항의 저작권 및 소유권은 해당 교육기관에 귀속됩니다. 무단 복제·배포를 엄금합니다.
                </div>
            </div>
        </div>
    </main>

    <!-- Custom Modal Dialogs -->
    <div id="custom-modal" class="no-print fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center hidden opacity-0 transition-opacity duration-300">
        <div class="bg-white rounded-2xl p-6 max-w-md w-full mx-4 shadow-2xl transform scale-95 transition-transform duration-300 space-y-4">
            <div class="flex items-center gap-3 border-b pb-3" id="modal-header-container">
                <i id="modal-icon" class="fa-solid fa-circle-info text-2xl text-indigo-600"></i>
                <h3 id="modal-title" class="text-md font-extrabold text-slate-950">알림</h3>
            </div>
            <p id="modal-message" class="text-xs text-slate-600 leading-relaxed"></p>
            <div class="flex justify-end gap-2" id="modal-actions">
                <button onclick="closeModal()" class="bg-slate-900 text-white font-bold text-xs px-4 py-2 rounded-lg">확인</button>
            </div>
        </div>
    </div>

    <!-- Live Toast Alert Panel -->
    <div id="toast" class="no-print fixed bottom-6 right-6 bg-slate-900 text-slate-200 text-xs px-4 py-3 rounded-xl border border-slate-800 shadow-2xl flex items-center gap-2 transform translate-y-20 opacity-0 transition-all duration-300 z-[100]">
        <i class="fa-solid fa-circle-check text-emerald-400 text-sm"></i>
        <span id="toast-text">저장되었습니다.</span>
    </div>

    <!-- CORE SYSTEM ENGINE SCRIPT -->
    <script>
        var isPaperTeacherMode = false;
        var currentLevel = localStorage.getItem('monthly_exam_level') || 'middle';
        
        var vocabCount = parseInt(localStorage.getItem('monthly_exam_vocab_count')) || 15;
        var vocabType = localStorage.getItem('monthly_exam_vocab_type') || 'matching';
        var readingCount = parseInt(localStorage.getItem('monthly_exam_reading_count')) || 1;
        var translationCount = parseInt(localStorage.getItem('monthly_exam_translation_count')) || 5;
        var unscrambleCount = parseInt(localStorage.getItem('monthly_exam_unscramble_count')) || 5;
        
        var examData = null;
        var apiKey = localStorage.getItem('monthly_exam_api_key') || '';

        const emojiDictionary = {
            "apple": "🍎", "사과": "🍎", "banana": "🍌", "바나나": "🍌", "cat": "🐱", "고양이": "🐱",
            "dog": "🐶", "개": "🐶", "강아지": "🐶", "sun": "☀️", "태양": "☀️", "해": "☀️",
            "tree": "🌳", "나무": "🌳", "car": "🚗", "자동차": "🚗", "book": "📖", "책": "📖",
            "milk": "🥛", "우유": "🥛", "fish": "🐟", "물고기": "🐟", "bird": "🐦", "새": "🐦"
        };

        function getEmojiForWord(word, mean) {
            const w = (word || "").toLowerCase().trim();
            const m = (mean || "").toLowerCase().trim();
            if (emojiDictionary[w]) return emojiDictionary[w];
            if (emojiDictionary[m]) return emojiDictionary[m];
            const defaults = ["⭐", "✏️", "🎈", "🌟", "🍀"];
            return defaults[(w.length + m.length) % defaults.length];
        }

        const defaultExamData = {
            elementary_junior: {
                vocab: [
                    { word: "apple", mean: "사과" }, { word: "dog", mean: "강아지" },
                    { word: "cat", mean: "고양이" }, { word: "sun", mean: "태양" },
                    { word: "tree", mean: "나무" }, { word: "car", mean: "자동차" },
                    { word: "book", mean: "책" }, { word: "milk", mean: "우유" },
                    { word: "fish", mean: "물고기" }, { word: "bird", mean: "새" }
                ],
                reading: [
                    {
                        passage: "Look at the sky! The sun is big and hot. ☀️ It is a beautiful day. Mimi, the cute white cat, is sleeping under the big green tree. A small blue bird is singing on the branch.",
                        questions: [
                            { q: "Mimi가 잠을 자고 있는 장소는 어디인가요?", type: "descriptive", questionCategory: "서술", choices: [], answer: null, answerText: "큰 초록색 나무 밑" },
                            { q: "위 글의 날씨 묘사로 어울리지 않는 것을 고르세요.", type: "mcq", questionCategory: "내용불일치", choices: ["화창하다", "아름답다", "매우덥다", "구름한점없음", "눈이내린다"], answer: 5, answerText: "" },
                            { q: "다음 제시된 단어 카드를 바르게 배열하여 문장을 쓰세요.", type: "unscramble", questionCategory: "배열", choices: [], answer: null, answerText: "Mimi opens her yellow eyes", shuffledWords: ["eyes", "her", "yellow", "Mimi", "opens"] }
                        ]
                    }
                ],
                translation: [
                    { eng: "I love my happy and sweet family very much.", kor: "나는 나의 행복하고 화목한 가족을 아주 많이 사랑한다." },
                    { eng: "The bright sun is shining in the blue sky today.", kor: "오늘 파란 하늘에 밝은 태양이 반짝반짝 빛나고 있다." },
                    { eng: "A cute little dog is running in the garden.", kor: "귀여운 아기 강아지 한 마리가 정원에서 뛰놀고 있다." },
                    { eng: "We eat fresh apples and yellow bananas every afternoon.", kor: "우리는 매일 오후에 싱싱한 사과와 노란 바나나를 먹는다." },
                    { eng: "The green tree has many pretty red flowers.", kor: "그 초록색 나무에는 예쁜 빨간 꽃들이 많이 피어 있다." }
                ],
                unscramble: [
                    { eng: "I have a red ball in my bag.", kor: "나는 가방 안에 빨간 공을 하나 가지고 있다." },
                    { eng: "The sky is very blue and beautiful today.", kor: "오늘 하늘은 매우 파랗고 눈부시게 아름답다." },
                    { eng: "She likes cute yellow birds on the tree.", kor: "그녀는 나무 위에 앉아 있는 귀여운 노란 새들을 좋아한다." },
                    { eng: "He rides his blue bicycle to school.", kor: "그는 그의 파란색 자전거를 타고 학교에 간다." },
                    { eng: "My dog waits for me at the door.", kor: "우리 강아지는 문 앞에서 나를 기다린다." }
                ]
            },
            elementary: { vocab: [], reading: [], translation: [], unscramble: [] },
            middle: { vocab: [], reading: [], translation: [], unscramble: [] }
        };

        function showToast(text) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-text').innerText = text;
            toast.className = toast.className.replace('translate-y-20 opacity-0', 'translate-y-0 opacity-100');
            setTimeout(() => { toast.className = toast.className.replace('translate-y-0 opacity-100', 'translate-y-20 opacity-0'); }, 3000);
        }

        function openModal(title, msg) {
            const modal = document.getElementById('custom-modal');
            document.getElementById('modal-title').innerText = title;
            document.getElementById('modal-message').innerText = msg;
            modal.classList.remove('hidden');
            setTimeout(() => { modal.classList.remove('opacity-0'); }, 5);
        }

        function closeModal() {
            document.getElementById('custom-modal').classList.add('hidden');
        }

        function changeLevel(level) {
            currentLevel = level;
            localStorage.setItem('monthly_exam_level', level);
            
            let englishExamName = "Premium Monthly Evaluation";
            if (level === 'elementary_junior' || level === 'elementary') {
                englishExamName = "Monthly Growth Challenge";
            }
            
            document.getElementById('config-title').value = englishExamName;
            updateSidebarLevelButtons();
            
            examData = JSON.parse(JSON.stringify(defaultExamData[level] || defaultExamData['elementary_junior']));
            localStorage.removeItem('monthly_exam_v3_data');
            
            initializeEditorInputs();
            syncHeaderData();
            renderPaperPreview();
            showToast(`대제목이 [ ${englishExamName} ] 으로 설정되었습니다.`);
        }

        function updateSidebarLevelButtons() {
            const btnElemJr = document.getElementById('sidebar-btn-elem-jr');
            const btnElem = document.getElementById('sidebar-btn-elem');
            const btnMid = document.getElementById('sidebar-btn-mid');
            btnElemJr.className = btnElem.className = btnMid.className = "py-1 px-1 bg-white text-slate-700 border border-slate-300 rounded font-semibold text-[10px] transition truncate";
            if (currentLevel === 'elementary_junior') btnElemJr.className = "py-1 px-1 bg-indigo-600 text-white font-bold rounded shadow text-[10px] truncate";
            else if (currentLevel === 'elementary') btnElem.className = "py-1 px-1 bg-indigo-600 text-white font-bold rounded shadow text-[10px] truncate";
            else btnMid.className = "py-1 px-1 bg-indigo-600 text-white font-bold rounded shadow text-[10px] truncate";
        }

        function syncCountControls() {
            document.getElementById('config-vocab-count').value = vocabCount;
            document.getElementById('sidebar-range-vocab').value = vocabCount;
            document.getElementById('sidebar-val-vocab').innerText = vocabCount + '개';
            document.getElementById('sidebar-vocab-type').value = vocabType;
            document.getElementById('config-vocab-type').value = vocabType;
            document.getElementById('config-reading-count').value = readingCount;
            document.getElementById('sidebar-range-reading').value = readingCount;
            document.getElementById('sidebar-val-reading').innerText = readingCount + '개';
            document.getElementById('config-translation-count').value = translationCount;
            document.getElementById('sidebar-range-translation').value = translationCount;
            document.getElementById('sidebar-val-translation').innerText = translationCount + '개';
            document.getElementById('config-unscramble-count').value = unscrambleCount;
            document.getElementById('sidebar-range-unscramble').value = unscrambleCount;
            document.getElementById('sidebar-val-unscramble').innerText = unscrambleCount + '개';
        }

        function changeVocabCount(val) { vocabCount = parseInt(val) || 5; syncCountControls(); syncHeaderData(); renderPaperPreview(); }
        function changeVocabType(val) { vocabType = val; syncCountControls(); renderPaperPreview(); }
        function changeReadingCount(val) { readingCount = parseInt(val) || 1; syncCountControls(); syncHeaderData(); initializeEditorInputs(); renderPaperPreview(); }
        function changeTranslationCount(val) { translationCount = parseInt(val) || 5; syncCountControls(); syncHeaderData(); renderPaperPreview(); }
        function changeUnscrambleCount(val) { unscrambleCount = parseInt(val) || 5; syncCountControls(); syncHeaderData(); renderPaperPreview(); }
        function toggleTeacherDrawer() { document.getElementById('teacher-drawer').classList.toggle('hidden'); }
        function saveApiKey(val) { apiKey = val.trim(); localStorage.setItem('monthly_exam_api_key', apiKey); }
        function formatScore(num) { return Number.isInteger(num) ? num.toFixed(0) : num.toFixed(1); }

        // 학원명 변경 싱크 유지
        function syncHeaderData() {
            const academy = document.getElementById('config-academy').value;
            const title = document.getElementById('config-title').value;
            const subject = document.getElementById('config-subject').value;
            const date = document.getElementById('config-date').value;

            document.getElementById('paper-academy-display').innerText = academy;
            document.getElementById('paper-title-display').innerText = title;
            document.getElementById('paper-subject-display').innerText = subject;
            document.getElementById('paper-date-display').innerText = date;

            const readingQuestionsCount = readingCount * 3;
            document.getElementById('paper-vocab-title-display').innerText = `[I] Vocabulary Evaluation (1 - ${vocabCount})`;
            document.getElementById('paper-vocab-score-display').innerText = `각 ${formatScore(100 / vocabCount)}점 [총 100점]`;
            document.getElementById('paper-reading-title-display').innerText = `[II] Reading Comprehension (${vocabCount + 1} - ${vocabCount + readingQuestionsCount})`;
            document.getElementById('paper-reading-score-display').innerText = `지문당 배점 분할 [총 100점]`;
            document.getElementById('paper-translation-title-display').innerText = `[III] Sentence Translation (${vocabCount + readingQuestionsCount + 1} - ${vocabCount + readingQuestionsCount + translationCount})`;
            document.getElementById('paper-translation-score-display').innerText = `각 ${formatScore(100 / translationCount)}점 [총 100점]`;
            document.getElementById('paper-unscramble-title-display').innerText = `[IV] Sentence Unscrambling Practice (${vocabCount + readingQuestionsCount + translationCount + 1} - ${vocabCount + readingQuestionsCount + translationCount + unscrambleCount})`;
            document.getElementById('paper-unscramble-score-display').innerText = `각 ${formatScore(100 / unscrambleCount)}점 [총 100점]`;

            document.getElementById('tab-vocab').innerText = `단어 (${vocabCount})`;
            document.getElementById('tab-reading').innerText = `독해 (${readingCount}지문)`;
            document.getElementById('tab-translation').innerText = `해석 (${translationCount})`;
            document.getElementById('tab-unscramble').innerText = `배열 (${unscrambleCount})`;
        }

        function initializeEditorInputs() {
            if (!examData) return;
            document.getElementById('edit-vocab-eng').value = (examData.vocab || []).map(x => x.word).join('\n');
            document.getElementById('edit-vocab-kor').value = (examData.vocab || []).map(x => x.mean).join('\n');
            
            const list = document.getElementById('reading-editor-list');
            list.innerHTML = '';
            for(let pIdx = 0; pIdx < readingCount; pIdx++) {
                if (!examData.reading[pIdx]) {
                    examData.reading[pIdx] = { passage: "지문을 적어주세요.", questions: [ {q:"",type:"mcq",choices:["","","","",""],answer:1,answerText:""},{q:"",type:"mcq",choices:["","","","",""],answer:1,answerText:""},{q:"",type:"descriptive",choices:[],answer:null,answerText:""} ] };
                }
                const pass = examData.reading[pIdx];
                const pBox = document.createElement('div');
                pBox.className = "bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2 text-xs text-white";
                pBox.innerHTML = `
                    <div class="flex justify-between font-bold text-amber-400"><span>[지문 ${pIdx+1} 편집 상자]</span></div>
                    <textarea id="edit-passage-${pIdx}" rows="3" class="w-full bg-slate-900 border p-2 text-slate-100 rounded font-serif">${pass.passage}</textarea>
                    <div class="text-[11px] text-slate-400 p-1">⚠️ 하위 문항은 일괄 출제 마법 구동 시 자동으로 정밀 연동 기입됩니다.</div>
                `;
                list.appendChild(pBox);
            }

            document.getElementById('edit-translation').value = (examData.translation || []).map(x => `${x.eng}=${x.kor}`).join('\n');
            document.getElementById('edit-unscramble').value = (examData.unscramble || []).map(x => `${x.eng}=${x.kor}`).join('\n');
        }

        function switchEditorTab(tab) {
            ['vocab', 'reading', 'translation', 'unscramble'].forEach(t => {
                document.getElementById(`tab-${t}`).className = "px-3 py-1.5 text-xs font-semibold text-slate-400 hover:text-white rounded-t-md";
                document.getElementById('panel-' + t).classList.add('hidden');
            });
            document.getElementById(`tab-${tab}`).className = "px-3 py-1.5 text-xs font-semibold text-white border-b-2 border-indigo-500 bg-slate-800 rounded-t-md";
            document.getElementById('panel-' + tab).classList.remove('hidden');
        }

        function handleVocabEngPaste(e) {
            const text = (e.clipboardData || window.clipboardData).getData('Text');
            if (text.includes('\t')) {
                e.preventDefault();
                const engs = []; const kors = [];
                text.split(/\r?\n/).forEach(l => {
                    let p = l.split('\t');
                    if(p[0]) engs.push(p[0].trim()); if(p[1]) kors.push(p[1].trim());
                });
                document.getElementById('edit-vocab-eng').value = engs.join('\n');
                document.getElementById('edit-vocab-kor').value = kors.join('\n');
            }
        }

        function applyVocabChange() {
            const engs = document.getElementById('edit-vocab-eng').value.split('\n');
            const kors = document.getElementById('edit-vocab-kor').value.split('\n');
            const arr = [];
            for (let i = 0; i < Math.max(engs.length, kors.length); i++) {
                if (engs[i] || kors[i]) arr.push({ word: (engs[i]||"").trim(), mean: (kors[i]||"").trim() });
            }
            examData.vocab = arr; renderPaperPreview(); showToast("단어가 반영되었습니다.");
        }

        function applyReadingChange() {
            for (let p = 0; p < readingCount; p++) {
                if(document.getElementById(`edit-passage-${p}`)) {
                    examData.reading[p].passage = document.getElementById(`edit-passage-${p}`).value.trim();
                }
            }
            renderPaperPreview(); showToast("독해 지문이 반영되었습니다.");
        }

        function applyTranslationChange() {
            const lines = document.getElementById('edit-translation').value.trim().split('\n');
            const arr = [];
            lines.forEach(line => {
                if (!line.includes('=')) return;
                const p = line.split('=');
                arr.push({ eng: p[0].trim(), kor: p[1].trim() });
            });
            if(arr.length > 0) {
                examData.translation = arr;
                renderPaperPreview();
                showToast("영한해석 데이터가 반영되었습니다.");
            } else {
                openModal("포맷 확인", "줄마다 문장 입력 시 문장 구조 '영어=한글뜻'을 유지해 주세요.");
            }
        }

        function applyUnscrambleChange() {
            const lines = document.getElementById('edit-unscramble').value.trim().split('\n');
            const arr = [];
            lines.forEach(line => {
                if (!line.includes('=')) return;
                const p = line.split('=');
                arr.push({ eng: p[0].trim(), kor: p[1].trim() });
            });
            if(arr.length > 0) {
                examData.unscramble = arr;
                renderPaperPreview();
                showToast("어순배열 데이터가 반영되었습니다.");
            } else {
                openModal("포맷 확인", "줄마다 문장 입력 시 문장 구조 '영어문장=한국어힌트'를 유지해 주세요.");
            }
        }

        function saveToLocalStorage() { localStorage.setItem('monthly_exam_v3_data', JSON.stringify(examData)); showToast("캐시에 저장되었습니다."); }
        function resetToDemo() { examData = JSON.parse(JSON.stringify(defaultExamData[currentLevel])); initializeEditorInputs(); renderPaperPreview(); }

        function renderPaperPreview() {
            if (!examData) return;
            const printSheet = document.getElementById('print-sheet');
            printSheet.className = currentLevel === 'elementary_junior' ? "paper-preview w-full max-w-[210mm] min-h-[297mm] p-8 md:p-12 relative bg-white junior-mode" : "paper-preview w-full max-w-[210mm] min-h-[297mm] p-8 md:p-12 relative bg-white";

            // 1. Vocab Section
            const vGrid = document.getElementById('paper-vocab-grid');
            const vMatchingContainer = document.getElementById('paper-vocab-matching-container');
            const activeVocab = [...(examData.vocab || []).slice(0, vocabCount)];
            while(activeVocab.length < vocabCount) activeVocab.push({ word: "________", mean: "________" });
            
            if (vocabType === 'matching') {
                vGrid.classList.add('hidden'); vMatchingContainer.classList.remove('hidden');
                document.getElementById('paper-vocab-instruction-display').innerHTML = `※ [선잇기] 왼쪽 그림 단어의 인덱스에 상응하는 우측 단어 카드로 선을 연결하세요.`;
                renderMatchingVocab(vMatchingContainer, activeVocab);
            } else {
                vGrid.classList.remove('hidden'); vMatchingContainer.classList.add('hidden');
                document.getElementById('paper-vocab-instruction-display').innerHTML = `※ 다음 제시된 문항 단어의 공란에 알맞은 올바른 해석 및 스펠링을 서술하시오.`;
                vGrid.innerHTML = '';
                activeVocab.forEach((item, idx) => {
                    const cell = document.createElement('div'); cell.className = "flex flex-col border border-slate-200 p-2.5 rounded-lg bg-slate-50/40 min-h-[60px]";
                    let isWordToMean = vocabType !== 'eng' ? (vocabType === 'mixed' ? idx % 2 === 0 : true) : false;
                    cell.innerHTML = `<div class="flex flex-col justify-between h-full text-[11px]">
                        <span class="text-slate-900 font-bold"><span class="text-[10px] text-slate-400 bg-slate-200 px-1 py-0.5 rounded-full mr-1">${idx + 1}</span>${isWordToMean ? item.word : item.mean}</span>
                        ${isPaperTeacherMode ? `<span class="teacher-answer border-t border-dashed pt-1 text-center">${isWordToMean ? item.mean : item.word}</span>` : '<span class="writing-line"></span>'}
                    </div>`;
                    vGrid.appendChild(cell);
                });
            }

            // 2. Reading Section
            const rList = document.getElementById('paper-reading-list'); rList.innerHTML = '';
            const activeReading = [...(examData.reading || []).slice(0, readingCount)];
            activeReading.forEach((pass, pIdx) => {
                const passBlock = document.createElement('div'); 
                passBlock.className = "avoid-break border border-slate-300 rounded-xl bg-white p-4 shadow-sm space-y-4";
                
                let qHtml = '';
                (pass.questions || []).forEach((q, qIdx) => {
                    const num = pIdx * 3 + vocabCount + 1 + qIdx;
                    let inner = '';
                    if (q.type === 'mcq' || !q.type) {
                        let choicesList = '';
                        (q.choices || []).forEach((c, cIdx) => {
                            choicesList += `<li ${isPaperTeacherMode && q.answer===(cIdx+1)?'class="teacher-answer bg-rose-50 px-1.5 rounded"':''}>${"①②③④⑤"[cIdx]} ${c}</li>`;
                        });
                        inner = `<ul class="grid grid-cols-1 sm:grid-cols-2 gap-1 text-[11px] text-slate-700 mt-1 pl-1">${choicesList}</ul>`;
                    } else if (q.type === 'unscramble') {
                        const chips = (q.shuffledWords || []).map(w=>`<span class="border bg-slate-50 px-2 py-0.5 rounded text-[10px] font-sans">${w}</span>`).join(' ');
                        inner = `<div class="mt-2 space-y-1"><div class="flex flex-wrap gap-1.5 border border-dashed p-2 rounded bg-slate-50">${chips}</div>${isPaperTeacherMode ? `<div class="teacher-answer text-xs pl-1">정답: ${q.answerText}</div>` : '<div class="writing-line"></div>'}</div>`;
                    } else {
                        inner = isPaperTeacherMode ? `<div class="teacher-answer bg-rose-50/40 p-1.5 rounded text-xs pl-1">정답 예시: ${q.answerText}</div>` : '<div class="writing-line"></div>';
                    }
                    qHtml += `<div class="pt-2"><p class="font-bold text-slate-900">${num}. ${q.q||'출제 문항'} <span class="text-[9px] bg-slate-100 text-slate-500 px-1 rounded border">${q.questionCategory||'독해'}</span></p>${inner}</div>`;
                });

                passBlock.innerHTML = `
                    <div class="bg-slate-50 p-4 border border-slate-200 rounded-xl text-[11.5px] font-serif leading-relaxed italic text-slate-800 relative">
                        <span class="font-bold text-indigo-900 not-italic block mb-2 text-xs"><i class="fa-solid fa-book-open text-indigo-600 mr-1"></i> [지문 및 독해 본문 ${pIdx+1}]</span>
                        ${pass.passage}
                    </div>
                    <div class="space-y-3 pt-2 divide-y border-t border-slate-100">${qHtml}</div>
                `;
                rList.appendChild(passBlock);
            });

            // 3. Translation Section
            const tList = document.getElementById('paper-translation-list'); tList.innerHTML = '';
            const activeTranslation = (examData.translation || []).slice(0, translationCount);
            activeTranslation.forEach((item, idx) => {
                const num = idx + vocabCount + (readingCount * 3) + 1;
                const row = document.createElement('div'); row.className = "avoid-break p-3 border border-slate-200 rounded-xl space-y-2 bg-slate-50/10";
                row.innerHTML = `<div class="font-bold text-slate-800 text-[11px]"><span class="text-[10px] bg-slate-200 text-slate-700 px-2 py-0.5 rounded-full mr-1">${num}</span> ${item.eng}</div>
                    ${isPaperTeacherMode ? `<div class="teacher-answer bg-rose-50/50 p-2 rounded text-xs">정답: ${item.kor}</div>` : '<div class="writing-line"></div>'}`;
                tList.appendChild(row);
            });

            // 4. Unscramble Section
            const uList = document.getElementById('paper-unscramble-list'); uList.innerHTML = '';
            const activeUnscramble = (examData.unscramble || []).slice(0, unscrambleCount);
            activeUnscramble.forEach((item, idx) => {
                const num = idx + vocabCount + (readingCount * 3) + translationCount + 1;
                const row = document.createElement('div'); row.className = "avoid-break p-3 border border-slate-200 rounded-xl space-y-2 bg-slate-50/10";
                const words = item.eng.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").split(/\s+/).filter(Boolean).sort((a,b)=>a.localeCompare(b));
                const chips = words.map(w => `<span class="border bg-white px-2 py-0.5 rounded text-[10.5px] font-sans font-medium shadow-sm">${w}</span>`).join(' ');
                row.innerHTML = `<div class="font-bold text-slate-800 text-[11px]"><span class="text-[10px] bg-slate-200 text-slate-700 px-2 py-0.5 rounded-full mr-1">${num}</span> [힌트: ${item.kor}]</div>
                    <div class="flex flex-wrap gap-1.5 py-2 border border-dashed rounded-lg px-2.5 bg-slate-50">${chips}</div>
                    ${isPaperTeacherMode ? `<div class="teacher-answer bg-rose-50/50 p-2 rounded text-xs">정답 문장: ${item.eng}</div>` : '<div class="writing-line"></div>'}`;
                uList.appendChild(row);
            });
        }

        function renderMatchingVocab(container, activeVocab) {
            container.innerHTML = ''; const chunkSize = 5;
            for (let chunkStart = 0; chunkStart < vocabCount; chunkStart += chunkSize) {
                const chunk = activeVocab.slice(chunkStart, chunkStart + chunkSize);
                const scrambled = [...chunk].sort((a, b) => a.word.localeCompare(b.word));
                const block = document.createElement('div'); block.className = "avoid-break relative border border-slate-200 p-4 rounded-2xl bg-slate-50/10";
                let lines = '';
                if (isPaperTeacherMode) {
                    chunk.forEach((item, lIdx) => {
                        let rIdx = scrambled.indexOf(item);
                        if (rIdx !== -1) lines += `<line x1="8%" y1="${(lIdx*20)+10}%" x2="92%" y2="${(rIdx*20)+10}%" stroke="#dc2626" stroke-width="2" stroke-dasharray="3 3"/>`;
                    });
                }
                let lHtml = ''; let rHtml = '';
                for (let i = 0; i < chunkSize; i++) {
                    if (!chunk[i]) continue;
                    lHtml += `<div class="h-11 flex items-center justify-between bg-white border px-3 rounded-xl w-[42%] relative"><span class="text-xs text-slate-400 font-bold">${chunkStart+i+1}</span><div class="flex items-center gap-1.5"><span class="text-base">${getEmojiForWord(chunk[i].word, chunk[i].mean)}</span><span class="text-[11px] font-bold">${chunk[i].mean}</span></div><div class="w-1.5 h-1.5 rounded-full bg-slate-400 absolute right-[-3px] top-5"></div></div>`;
                    rHtml += `<div class="h-11 flex items-center bg-white border px-3 rounded-xl w-[42%] relative"><div class="w-1.5 h-1.5 rounded-full bg-slate-400 absolute left-[-3px] top-5"></div><span class="text-[11px] font-bold uppercase tracking-wide truncate ml-1">${scrambled[i].word}</span></div>`;
                }
                block.innerHTML = `<div class="absolute inset-0 w-full h-full pointer-events-none" style="z-index:10;"><svg class="w-full h-full">${lines}</svg></div>
                    <div class="flex justify-between items-center h-72 relative">
                        <div class="flex flex-col justify-between h-full w-full">${lHtml.split('</div>').filter(Boolean).map(c=>`<div class="flex justify-between items-center">${c}</div>`).join('')}</div>
                        <div class="absolute right-0 top-0 bottom-0 left-0 flex flex-col justify-between pointer-events-none">${rHtml.split('</div>').filter(Boolean).map(c=>`<div class="flex justify-end items-center">${c}</div>`).join('')}</div>
                    </div>`;
                container.appendChild(block);
            }
        }

        function togglePaperAnswerView(isTeacher) {
            isPaperTeacherMode = isTeacher;
            document.getElementById('paper-btn-student').className = isTeacher ? "py-1.5 bg-slate-100 text-slate-700 font-semibold text-xs rounded" : "py-1.5 bg-indigo-600 text-white font-bold text-xs rounded shadow";
            document.getElementById('paper-btn-teacher').className = isTeacher ? "py-1.5 bg-indigo-600 text-white font-bold text-xs rounded shadow" : "py-1.5 bg-slate-100 text-slate-700 font-semibold text-xs rounded";
            renderPaperPreview();
        }

        function togglePageBreak(elementId) {
            const el = document.getElementById(elementId);
            if(!el) return;
            if(el.classList.contains('print-page-break')) {
                el.className = ""; el.innerHTML = "";
            } else {
                el.className = "print-page-break border-t border-dashed border-amber-400 my-4 relative";
                el.innerHTML = `<span class="page-break-indicator absolute -top-2.5 left-2 bg-amber-400 text-slate-950 px-1.5 py-0.5 rounded text-[8px] font-bold">다음 페이지 분절점</span>`;
            }
        }

        function triggerPrint() { window.print(); }

        // AI CORE ENGINE
        async function generateAIQuestionsForPassage(pIdx) {
            const txt = document.getElementById(`edit-passage-${pIdx}`).value.trim();
            if (!txt || txt.length < 10 || !apiKey) return;
            const overlay = document.getElementById('ai-loading-overlay');
            overlay.classList.remove('hidden');
            const prompt = `지문: "${txt}" 기반 3문제 출제 스키마 규격 리턴: [{"q":"질문","type":"mcq","choices":["1","2","3","4","5"],"answer":1,"answerText":"","shuffledWords":[]}]`;
            const result = await makeGeminiCallWithRetry({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { responseMimeType: "application/json" } });
            overlay.classList.add('hidden');
            if (result) {
                try {
                    examData.reading[pIdx] = { passage: txt, questions: JSON.parse(result).slice(0, 3) };
                    initializeEditorInputs(); syncHeaderData(); renderPaperPreview();
                } catch (e) { console.log(e); }
            }
        }

        async function generateAIQuestionsAllPassages() {
            const passages = [];
            for (let i = 0; i < readingCount; i++) {
                const txt = document.getElementById(`edit-passage-${i}`)?.value.trim() || "";
                passages.push({ id: i, text: txt });
            }
            if (!apiKey) return;
            const overlay = document.getElementById('ai-loading-overlay'); overlay.classList.remove('hidden');
            const prompt = `각 지문별로 최적의 3문항씩 총 ${readingCount * 3}문항을 생성하세요. JSON 구조 리턴: {"reading":[{"passageId":0,"questions":[{"q":"질문","type":"mcq","choices":["1","2","3","4","5"],"answer":1,"answerText":"","shuffledWords":[]}]}]}: \n ${JSON.stringify(passages)}`;
            const result = await makeGeminiCallWithRetry({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { responseMimeType: "application/json" } });
            overlay.classList.add('hidden');
            if (result) {
                try {
                    JSON.parse(result).reading.forEach(item => {
                        if (examData.reading[item.passageId]) examData.reading[item.passageId].questions = item.questions;
                    });
                    initializeEditorInputs(); syncHeaderData(); renderPaperPreview();
                } catch (e) { console.log(e); }
            }
        }

        async function makeGeminiCallWithRetry(payload) {
            let attempt = 0;
            while (attempt < 3) {
                try {
                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
                        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
                    });
                    const json = await response.json();
                    return json.candidates?.[0]?.content?.parts?.[0]?.text;
                } catch (e) { attempt++; }
            }
            return null;
        }

        window.onload = function() {
            const cached = localStorage.getItem('monthly_exam_v3_data');
            if (cached) examData = JSON.parse(cached);
            else examData = JSON.parse(JSON.stringify(defaultExamData[currentLevel]));
            
            let initialExamName = currentLevel === 'middle' ? "Premium Monthly Evaluation" : "Monthly Growth Challenge";
            document.getElementById('config-title').value = initialExamName;

            syncCountControls();
            updateSidebarLevelButtons();
            initializeEditorInputs();
            syncHeaderData();
            renderPaperPreview();
        };
    </script>
</body>
</html>
