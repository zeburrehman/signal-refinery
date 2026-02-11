import { HealthCheck } from "@/components/HealthCheck";

export default function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Welcome to Signal Refinery UI
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            A modern, type-safe application built with Next.js and TypeScript
          </p>
        </div>
      </section>

      {/* Health Check Section */}
      <section>
        <HealthCheck />
      </section>

      {/* Features Section */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-8">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="rounded-lg border border-gray-200 bg-white p-6">
            <h3 className="font-semibold text-gray-900">Type Safe</h3>
            <p className="mt-2 text-sm text-gray-600">
              Full TypeScript support for better developer experience
            </p>
          </div>
          <div className="rounded-lg border border-gray-200 bg-white p-6">
            <h3 className="font-semibold text-gray-900">Tailwind CSS</h3>
            <p className="mt-2 text-sm text-gray-600">
              Utility-first CSS for rapid UI development
            </p>
          </div>
          <div className="rounded-lg border border-gray-200 bg-white p-6">
            <h3 className="font-semibold text-gray-900">Best Practices</h3>
            <p className="mt-2 text-sm text-gray-600">
              Organized project structure and conventions
            </p>
          </div>
        </div>
      </section>

      {/* Getting Started Section */}
      <section className="rounded-lg border border-gray-200 bg-white p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Getting Started</h2>
        <div className="space-y-4 text-sm text-gray-600">
          <p>
            <strong className="text-gray-900">Project Structure:</strong>
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>
              <code className="bg-gray-100 px-2 py-1 rounded">src/components</code> - Reusable React components
            </li>
            <li>
              <code className="bg-gray-100 px-2 py-1 rounded">src/hooks</code> - Custom React hooks
            </li>
            <li>
              <code className="bg-gray-100 px-2 py-1 rounded">src/lib</code> - Utility library functions
            </li>
            <li>
              <code className="bg-gray-100 px-2 py-1 rounded">src/types</code> - TypeScript type definitions
            </li>
            <li>
              <code className="bg-gray-100 px-2 py-1 rounded">src/constants</code> - Application constants
            </li>
          </ul>
        </div>
      </section>
    </div>
  );
}
