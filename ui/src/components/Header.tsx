/**
 * Header Component
 * Main navigation header
 */

export function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <nav className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900">Signal Refinery UI</h1>
          <ul className="flex gap-6">
            <li>
              <a href="/" className="text-gray-600 hover:text-gray-900">
                Home
              </a>
            </li>
            <li>
              <a href="/dashboard" className="text-gray-600 hover:text-gray-900">
                Dashboard
              </a>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  );
}
