import { useState, useEffect } from 'react'
import { Search, Share2, ExternalLink, Menu, Bell } from 'lucide-react'

interface Article {
    id: string
    title: string
    url: string
    source: string
    published_at: string
    summary: string
    tags: string[]
    is_saved: boolean
}

function App() {
    const [articles, setArticles] = useState<Article[]>([])
    const [savedIds, setSavedIds] = useState<Set<string>>(new Set())
    const [filter, setFilter] = useState<'all' | 'saved'>('all')

    useEffect(() => {
        const saved = localStorage.getItem('savedArticles')
        if (saved) {
            setSavedIds(new Set(JSON.parse(saved)))
        }

        fetch('/data.json')
            .then(res => res.json())
            .then(data => {
                setArticles(data.articles || [])
            })
            .catch(err => console.error("Failed to load articles", err))
    }, [])

    const toggleSave = (id: string) => {
        const newSaved = new Set(savedIds)
        if (newSaved.has(id)) {
            newSaved.delete(id)
        } else {
            newSaved.add(id)
        }
        setSavedIds(newSaved)
        localStorage.setItem('savedArticles', JSON.stringify(Array.from(newSaved)))
    }

    const displayedArticles = articles.filter(a => {
        if (filter === 'saved') return savedIds.has(a.id)
        return true
    })

    return (
        <div className="min-h-screen bg-background text-foreground font-sans">
            {/* Top Navbar */}
            <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-border">
                <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
                    {/* Logo Area */}
                    <div className="flex items-center gap-6">
                        <button className="p-2 hover:bg-muted rounded-full">
                            <Menu className="w-6 h-6" />
                        </button>
                        <div className="w-8 h-8 rounded-full border-2 border-black flex items-center justify-center font-bold text-lg">
                            T
                        </div>
                    </div>

                    {/* Nav Links / Tags - Horizontal Scroll */}
                    <div className="hidden md:flex items-center gap-6 overflow-x-auto text-sm font-medium text-muted-foreground no-scrollbar">
                        <button className="text-black font-semibold"># Popular</button>
                        <button className="hover:text-black transition-colors"># Favorite</button>
                        <button className="hover:text-black transition-colors"># Politics</button>
                        <button className="hover:text-black transition-colors"># Tech</button>
                        <button className="hover:text-black transition-colors"># Business</button>
                        <button className="hover:text-black transition-colors"># Science</button>
                    </div>

                    {/* Search */}
                    <div className="flex items-center gap-4">
                        <div className="relative hidden sm:block">
                            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                            <input
                                type="text"
                                placeholder="Search"
                                className="pl-10 pr-4 py-2 rounded-full border border-border bg-white text-sm focus:outline-none focus:ring-2 focus:ring-black/5"
                            />
                        </div>
                        <button className="p-2 hover:bg-muted rounded-full">
                            <Bell className="w-5 h-5" />
                        </button>
                        <div className="w-8 h-8 rounded-full bg-black"></div>
                    </div>
                </div>
            </header>

            {/* Sub Nav / Filters */}
            <div className="max-w-7xl mx-auto px-6 py-8">
                <div className="flex items-center gap-3">
                    <button className="bg-black text-white px-5 py-2 rounded-full text-sm font-medium shadow-lg hover:bg-black/90 transition-all">
                        + add collection
                    </button>
                    <button
                        onClick={() => setFilter('all')}
                        className={`px-6 py-2 rounded-full text-sm font-medium border transition-all ${filter === 'all' ? 'border-black text-black' : 'border-border text-muted-foreground hover:border-gray-400'}`}
                    >
                        news
                    </button>
                    <button
                        onClick={() => setFilter('saved')}
                        className={`px-6 py-2 rounded-full text-sm font-medium border transition-all ${filter === 'saved' ? 'border-black text-black' : 'border-border text-muted-foreground hover:border-gray-400'}`}
                    >
                        saved ({savedIds.size})
                    </button>
                </div>
            </div>

            {/* Masonry-style Grid */}
            <main className="max-w-7xl mx-auto px-6 pb-20">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
                    {displayedArticles.map(article => (
                        <article key={article.id} className="group flex flex-col h-full bg-white hover:bg-muted/30 transition-colors p-4 -mx-4 rounded-xl">
                            {/* Header: Source Pill + Team/Pro + Actions */}
                            <div className="flex items-center justify-between mb-4">
                                <div className="flex items-center gap-3">
                                    <div className={`w-3 h-3 rounded-full ${article.source === 'TheRundown' ? 'bg-blue-500' : article.source === 'Reddit' ? 'bg-orange-500' : 'bg-green-500'}`}></div>
                                    <span className="font-bold text-sm">{article.source}</span>
                                    <span className="text-[10px] font-bold text-muted-foreground tracking-widest uppercase">
                                        PRO
                                    </span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <button className="flex items-center gap-1 px-3 py-1 rounded-full border border-border text-xs font-medium hover:bg-muted transition-colors">
                                        <Share2 className="w-3 h-3" /> Share
                                    </button>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            toggleSave(article.id);
                                        }}
                                        className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium transition-colors ${savedIds.has(article.id) ? 'bg-black text-white' : 'bg-black text-white hover:bg-black/80'}`}
                                    >
                                        {savedIds.has(article.id) ? 'Saved' : 'Collect'}
                                    </button>
                                </div>
                            </div>

                            {/* Tags */}
                            {article.tags && article.tags.length > 0 && (
                                <div className="flex gap-2 mb-3">
                                    {article.tags.map((tag, i) => (
                                        <span key={i} className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded text-white ${i % 2 === 0 ? 'bg-indigo-500' : 'bg-pink-500'}`}>
                                            {tag}
                                        </span>
                                    ))}
                                </div>
                            )}

                            {/* Content */}
                            <a href={article.url} target="_blank" rel="noopener noreferrer" className="block group-hover:opacity-80 transition-opacity">
                                <h2 className="text-2xl font-bold leading-tight mb-3 tracking-tight">
                                    {article.title}
                                </h2>
                                <p className="text-muted-foreground text-sm leading-relaxed mb-4 line-clamp-3">
                                    {article.summary || "No summary available. Click to read the full insight from the source."}
                                </p>
                            </a>

                            {/* Footer */}
                            <div className="mt-auto pt-4 flex items-center justify-between text-muted-foreground text-xs font-medium border-t border-border/40">
                                <div className="flex items-center gap-4">
                                    <span className="flex items-center gap-1">
                                        ☺ 5.4
                                    </span>
                                    <span>
                                        {new Date(article.published_at).toLocaleDateString()}
                                    </span>
                                </div>
                                <a href={article.url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 hover:text-black">
                                    original <ExternalLink className="w-3 h-3" />
                                </a>
                            </div>
                        </article>
                    ))}
                </div>
            </main>
        </div>
    )
}

export default App
