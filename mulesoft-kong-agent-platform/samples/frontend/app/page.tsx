import type { CSSProperties } from 'react';

type Item = { api: string; events: number; cost_usd: string };
type Health = { status: string; demo_auth: boolean; entra_env_present: boolean };

export const dynamic = 'force-dynamic';

const API = process.env.API_INTERNAL_URL ?? 'http://localhost:8000';
// Local demo identity only — the backend accepts these headers solely when DEMO_AUTH=true.
const DEMO_HEADERS = { 'X-Demo-Agent': 'dashboard-demo', 'X-Demo-Department': 'it' };

// Vivid per-API palette: [fill gradient, glow, solid for donut/legend]
const PALETTE: [string, string, string][] = [
  ['linear-gradient(90deg,#8b5cf6,#e879f9)', 'rgba(232,121,249,.55)', '#c084fc'],
  ['linear-gradient(90deg,#06b6d4,#3b82f6)', 'rgba(34,211,238,.55)', '#22d3ee'],
  ['linear-gradient(90deg,#84cc16,#10b981)', 'rgba(163,230,53,.5)', '#a3e635'],
  ['linear-gradient(90deg,#f59e0b,#f43f5e)', 'rgba(251,191,36,.5)', '#fbbf24'],
  ['linear-gradient(90deg,#ec4899,#f97316)', 'rgba(236,72,153,.5)', '#f472b6'],
  ['linear-gradient(90deg,#14b8a6,#6366f1)', 'rgba(20,184,166,.5)', '#2dd4bf'],
];

const vars = (v: Record<string, string>) => v as CSSProperties;
const usd = (n: number) =>
  `$${n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: n < 1 ? 4 : 2 })}`;

async function load() {
  let items: Item[] = [];
  let department = 'it';
  let error = '';
  let health: Health | null = null;
  try {
    const r = await fetch(`${API}/api/v1/usage`, { headers: DEMO_HEADERS, cache: 'no-store' });
    if (!r.ok) throw new Error(`API HTTP ${r.status}`);
    const data = await r.json();
    items = data.items ?? [];
    department = data.department ?? department;
  } catch (e) {
    error = String(e);
  }
  try {
    const h = await fetch(`${API}/health`, { cache: 'no-store' });
    if (h.ok) health = await h.json();
  } catch {
    /* health is informational only */
  }
  return { items, department, error, health };
}

export default async function Page() {
  const { items, department, error, health } = await load();

  const rows = items
    .map((x, i) => ({ ...x, cost: Number(x.cost_usd) || 0, color: PALETTE[i % PALETTE.length] }))
    .sort((a, b) => b.cost - a.cost);
  const totalCost = rows.reduce((s, r) => s + r.cost, 0);
  const totalEvents = rows.reduce((s, r) => s + r.events, 0);
  const maxCost = Math.max(...rows.map((r) => r.cost), 0);
  const avgCost = totalEvents ? totalCost / totalEvents : 0;

  // Donut segments via conic-gradient
  let acc = 0;
  const ring =
    totalCost > 0
      ? `conic-gradient(${rows
          .map((r) => {
            const start = acc;
            acc += (r.cost / totalCost) * 100;
            return `${r.color[2]} ${start}% ${acc}%`;
          })
          .join(',')})`
      : 'conic-gradient(rgba(255,255,255,.08) 0 100%)';

  const now = new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo', hour12: false });
  const mode = health ? (health.demo_auth ? 'デモ認証' : 'Entra 認証') : '不明';

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <div className="logo" aria-hidden="true">A</div>
          <div>
            <h1>
              <span className="grad">Agent API</span> コストコンソール
            </h1>
            <p>MuleSoft × Kong × AI-Agent ガバナンス — ローカルデモ</p>
          </div>
        </div>
        <div className="pills">
          <span className="pill">
            <span className={`dot ${error ? 'bad' : ''}`} />
            API <strong>{error ? 'エラー' : '稼働中'}</strong>
          </span>
          <span className="pill">
            <span className={`dot ${health?.demo_auth ? 'warn' : ''}`} />
            <strong>{mode}</strong>
          </span>
          <span className="pill">
            部門 <strong>{department}</strong>
          </span>
          <a className="refresh" href="/">
            ↻ 更新
          </a>
        </div>
      </header>

      {error && (
        <div className="alert" role="alert">
          <span aria-hidden="true">⚠️</span>
          <div>
            <b>利用データを取得できませんでした</b>
            <div>
              <code>{error}</code>
            </div>
          </div>
        </div>
      )}

      <section className="kpis" aria-label="主要指標">
        <div className="card kpi k1">
          <div className="label">推定コスト合計</div>
          <div className="value">{usd(totalCost)}</div>
          <div className="sub">本日までの累計（USD）</div>
        </div>
        <div className="card kpi k2">
          <div className="label">イベント数</div>
          <div className="value">{totalEvents.toLocaleString('ja-JP')}</div>
          <div className="sub">記録された利用イベント</div>
        </div>
        <div className="card kpi k3">
          <div className="label">利用 API</div>
          <div className="value">{rows.length}</div>
          <div className="sub">コストが発生した API 数</div>
        </div>
        <div className="card kpi k4">
          <div className="label">平均単価</div>
          <div className="value">{usd(avgCost)}</div>
          <div className="sub">1 イベントあたり</div>
        </div>
      </section>

      <section className="grid">
        <div className="card panel">
          <h2>API 別コスト</h2>
          <p className="hint">最もコストの高い API を基準にした相対値</p>
          {rows.length === 0 ? (
            <div className="empty">まだ利用データがありません</div>
          ) : (
            <div className="bars">
              {rows.map((r) => (
                <div className="bar-row" key={r.api}>
                  <span className="bar-name" title={r.api}>
                    {r.api}
                  </span>
                  <div className="bar-track">
                    <div
                      className="bar-fill"
                      style={vars({
                        width: `${maxCost ? Math.max((r.cost / maxCost) * 100, 2) : 0}%`,
                        '--c': r.color[0],
                        '--glow': r.color[1],
                      })}
                    />
                  </div>
                  <span className="bar-val">{usd(r.cost)}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card panel">
          <h2>コスト構成比</h2>
          <p className="hint">部門 {department} の API 別シェア</p>
          <div className="donut-wrap">
            <div className="donut" style={vars({ '--ring': ring })} role="img" aria-label="API 別コスト構成比">
              <div className="donut-hole">
                <div>
                  <b>{usd(totalCost)}</b>
                  <small>合計</small>
                </div>
              </div>
            </div>
            {rows.length > 0 && (
              <ul className="legend">
                {rows.map((r) => (
                  <li key={r.api}>
                    <span className="sw" style={vars({ '--c': r.color[2] })} />
                    {r.api}
                    <span className="pct">{totalCost ? ((r.cost / totalCost) * 100).toFixed(1) : '0.0'}%</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </section>

      <section className="card panel">
        <h2>API 別明細</h2>
        <p className="hint">利用イベントと推定コストの内訳</p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>API</th>
                <th className="num">イベント数</th>
                <th className="num">推定 USD</th>
                <th className="num">シェア</th>
              </tr>
            </thead>
            <tbody>
              {rows.length === 0 ? (
                <tr>
                  <td colSpan={4} className="empty">
                    データなし
                  </td>
                </tr>
              ) : (
                rows.map((r) => (
                  <tr key={r.api}>
                    <td>
                      <span className="api-chip">
                        <i style={vars({ '--c': r.color[2], '--glow': r.color[1] })} />
                        {r.api}
                      </span>
                    </td>
                    <td className="num">{r.events.toLocaleString('ja-JP')}</td>
                    <td className="num">{usd(r.cost)}</td>
                    <td className="num">{totalCost ? ((r.cost / totalCost) * 100).toFixed(1) : '0.0'}%</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      <p className="footnote">
        最終更新 {now}（JST）· ローカルデモ用の表示です。実際の本番認証・認可・課金ではありません。
      </p>
    </main>
  );
}
