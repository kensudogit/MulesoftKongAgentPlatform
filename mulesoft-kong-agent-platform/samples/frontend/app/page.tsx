type Item = {api:string;events:number;cost_usd:string};
export const dynamic = 'force-dynamic';
export default async function Page() {
  let items:Item[]=[]; let error='';
  try {
    const r=await fetch(`${process.env.API_INTERNAL_URL ?? 'http://localhost:8000'}/api/v1/usage`,{headers:{'X-Demo-Agent':'dashboard-demo','X-Demo-Department':'it'},cache:'no-store'});
    if(!r.ok) throw new Error(`API HTTP ${r.status}`);
    const data=await r.json(); items=data.items;
  } catch(e) {error=String(e);}
  return <main><h1>AI-Agent API コスト可視化（ローカルデモ）</h1><p>部門: it / 実際の本番認証・認可・課金ではありません。</p>{error?<p role="alert">取得エラー: {error}</p>:<table cellPadding="12" border={1}><thead><tr><th>API</th><th>イベント数</th><th>推定USD</th></tr></thead><tbody>{items.map(x=><tr key={x.api}><td>{x.api}</td><td>{x.events}</td><td>{x.cost_usd}</td></tr>)}</tbody></table>}</main>;
}
