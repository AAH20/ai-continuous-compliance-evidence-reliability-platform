'use client';

import { useEffect, useState } from 'react';
import {
  Activity, ArrowRight, ArrowUpRight, CheckCircle2, CircleAlert, CloudCog,
  DatabaseZap, Download, GitBranch, Network, RotateCcw, ShieldCheck, TimerReset,
} from 'lucide-react';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const controls = [
  { id: 'IAM-04', name: 'Privileged access review', slo: 99.9, current: 99.96, budget: 61, state: 'healthy' },
  { id: 'LOG-02', name: 'Audit-log population coverage', slo: 99.5, current: 98.72, budget: 0, state: 'burning' },
  { id: 'CHG-07', name: 'Production change approval', slo: 99.0, current: 99.31, budget: 34, state: 'watch' },
];

const gates = [
  ['Provenance', '100.00%', 'pass'], ['Integrity', '100.00%', 'pass'], ['Scope', '99.42%', 'warn'],
  ['Freshness', '99.86%', 'pass'], ['Relevance', '98.74%', 'pass'], ['Temporal validity', '99.91%', 'pass'],
];

const sources = [
  ['AWS Organizations', '12 / 12 accounts', 'healthy', '44s'],
  ['AWS Config', '12 / 12 accounts', 'healthy', '01m'],
  ['Kubernetes audit', '7 / 8 clusters', 'degraded', '06m'],
  ['CI/CD change records', '5 / 5 pipelines', 'healthy', '38s'],
  ['Identity provider', '1 / 1 tenant', 'healthy', '02m'],
];

const assurancePack = {
  status: 'synthetic_reference', generated_at: '2026-09-07T09:30:00Z',
  control_slo: { population_recall: 0.9942, false_compliant_escape: 0.0008, evidence_mttd_seconds: 222 },
  incident: { id: 'INC-LOG-02', scope_gap: 'k8s-us-east-2', affected_assertions: 4, affected_assurance_requests: 2 },
  economics: { confirmed_value_exposed: 420000, modeled_pipeline_influenced: 210000, finance_approved_margin: 0 },
};

function Metric({ label, value, detail, tone = 'cyan' }: { label: string; value: string; detail: string; tone?: 'cyan' | 'amber' | 'green' }) {
  return <article className="metric-card"><div className={`metric-signal ${tone}`} /><p>{label}</p><strong>{value}</strong><span>{detail}</span></article>;
}

function downloadPack() {
  const blob = new Blob([JSON.stringify(assurancePack, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob); const anchor = document.createElement('a');
  anchor.href = url; anchor.download = 'controlsre-synthetic-assurance-pack.json'; anchor.click(); URL.revokeObjectURL(url);
}

export default function Home() {
  const [view, setView] = useState('operations');

  useEffect(() => {
    const context = typeof document === 'undefined' ? undefined : document.modelContext;
    if (!context?.registerTool) return;
    const lifecycle = new AbortController();
    void Promise.resolve(context.registerTool({
      name: 'select_controlsre_view', title: 'Select ControlSRE view',
      description: 'Open one of the visible ControlSRE workspaces: operations, evidence, economics, or evolution.',
      inputSchema: { type: 'object', properties: { view: { type: 'string', enum: ['operations', 'evidence', 'economics', 'evolution'] } }, required: ['view'], additionalProperties: false },
      annotations: { readOnlyHint: true, untrustedContentHint: false },
      execute(input: unknown) {
        const requested = (input as { view?: string })?.view;
        if (!requested || !['operations', 'evidence', 'economics', 'evolution'].includes(requested)) throw new Error('Unsupported ControlSRE view.');
        setView(requested); return { selected_view: requested };
      },
    }, { signal: lifecycle.signal })).catch(() => undefined);
    return () => lifecycle.abort();
  }, []);

  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="topbar">
        <div className="brand-mark"><ShieldCheck size={20} /><span><small>A2Z SOC / EVIDENCE RELIABILITY</small><b>ControlSRE</b></span></div>
        <div className="topbar-copy"><b>Reliability command</b><span>Production · 90-day audit window</span></div>
        <div className="ml-auto flex items-center gap-3"><Badge variant="outline">Synthetic reference</Badge><Badge className="live-badge"><Activity size={12} /> Live</Badge><Button variant="outline" size="sm" onClick={downloadPack}><Download /> Export assurance pack</Button></div>
      </header>

      <div className="workspace">
        <section className="status-strip" aria-label="Platform status">
          <div><CloudCog /><span><small>Sources</small><b>48 / 49 reporting</b></span></div>
          <div><DatabaseZap /><span><small>Qualified evidence</small><b>18,492 artifacts</b></span></div>
          <div><GitBranch /><span><small>Framework surface</small><b>167+ adapter-ready</b></span></div>
          <div className="incident-status"><CircleAlert /><span><small>Open reliability incident</small><b>1 scope degradation</b></span></div>
        </section>

        <Tabs value={view} onValueChange={setView} className="mt-7">
          <TabsList variant="line" className="border-b border-white/8">
            <TabsTrigger value="operations">Operations</TabsTrigger><TabsTrigger value="evidence">Evidence quality</TabsTrigger>
            <TabsTrigger value="economics">Board economics</TabsTrigger><TabsTrigger value="evolution">Evolution loop</TabsTrigger>
          </TabsList>

          <TabsContent value="operations" className="pt-6">
            <div className="metrics-grid">
              <Metric label="Population recall" value="99.42%" detail="Target ≥99.00%" /><Metric label="False-compliant escape" value="0.08%" detail="Target ≤0.10%" tone="green" />
              <Metric label="Evidence MTTD" value="03:42" detail="Target <05:00" tone="green" /><Metric label="Error-budget burn" value="2.8×" detail="LOG-02 · action required" tone="amber" />
            </div>
            <div className="main-grid">
              <section className="panel">
                <div className="panel-heading"><div><p className="eyebrow">Control reliability</p><h1>Where assurance is losing certainty</h1></div><Badge variant="outline">3 critical controls</Badge></div>
                <div className="control-list">{controls.map((control) => <article key={control.id} className="control-row"><div className="control-id">{control.id}</div><div className="control-main"><div><b>{control.name}</b><span>{control.current}% current · {control.slo}% SLO</span></div><Progress value={Math.min(control.budget, 100)} className={`progress-${control.state}`} /></div><div className={`state-dot ${control.state}`}><span />{control.state === 'burning' ? 'Budget exhausted' : `${control.budget}% budget`}</div></article>)}</div>
              </section>
              <aside className="panel impact-panel">
                <p className="eyebrow">Decision impact</p><h2>LOG-02 needs intervention</h2><p className="muted">One Kubernetes cluster stopped reporting after a collector permission change. A green control result is blocked until scope is restored.</p>
                <div className="impact-chain"><span>1 source gap</span><ArrowUpRight /><span>4 control assertions</span><ArrowUpRight /><span>2 assurance requests</span></div>
                <div className="impact-values"><div><small>Confirmed value exposed</small><strong>$420K</strong></div><div><small>Finance-attributable margin</small><strong>$0</strong></div></div>
                <p className="guardrail"><ShieldCheck size={15} />Contract value is context, not ROI, until Finance approves attribution.</p>
                <Dialog><DialogTrigger render={<Button className="w-full" />}>Open incident evidence</DialogTrigger><DialogContent className="border-white/10 bg-[#111827] text-slate-100"><DialogHeader><DialogTitle>INC-LOG-02 · Scope degradation</DialogTitle><DialogDescription>Detected by expected-versus-observed population reconciliation.</DialogDescription></DialogHeader><div className="dialog-grid"><span>Affected source</span><b>k8s-us-east-2</b><span>Trigger</span><b>Collector authorization loss</b><span>Fail-closed action</span><b>4 assertions marked unknown</b><span>Required recovery</span><b>Restore permission, recollect, replay</b></div></DialogContent></Dialog>
              </aside>
            </div>
          </TabsContent>

          <TabsContent value="evidence" className="pt-6">
            <div className="section-grid"><section className="panel"><p className="eyebrow">Qualification gates</p><h2 className="section-title">Evidence must pass every material gate</h2><div className="gate-grid">{gates.map(([name,value,state]) => <div key={name} className="gate-card"><span className={`gate-icon ${state}`}><CheckCircle2 /></span><div><small>{name}</small><strong>{value}</strong></div><Badge variant="outline">{state === 'pass' ? 'PASS' : 'DEGRADED'}</Badge></div>)}</div></section><section className="panel"><p className="eyebrow">Population reconciliation</p><h2 className="section-title">Expected sources versus observed evidence</h2><div className="source-list">{sources.map(([name,scope,state,lag]) => <div key={name}><span><b>{name}</b><small>{scope}</small></span><Badge variant="outline" className={state === 'degraded' ? 'warn-badge' : 'ok-badge'}>{state}</Badge><code>{lag}</code></div>)}</div></section></div>
            <section className="panel lineage-panel"><div><p className="eyebrow">Evidence lineage</p><h2 className="section-title">A receipt survives every decision boundary</h2></div><div className="lineage">{['Source inventory','Collection receipt','Six qualification gates','Temporal control graph','OSCAL result','Human decision'].map((item,index)=><div key={item}><span>{String(index+1).padStart(2,'0')}</span><b>{item}</b>{index<5&&<ArrowRight />}</div>)}</div></section>
          </TabsContent>

          <TabsContent value="economics" className="pt-6">
            <div className="metrics-grid economics-metrics"><Metric label="Cost / qualified evidence" value="$3.84" detail="All-in reference cost" /><Metric label="Audit rework avoided" value="$104K" detail="Verified annualized model" tone="green" /><Metric label="Confirmed value exposed" value="$420K" detail="Context only · excluded from ROI" tone="amber" /><Metric label="Finance-approved margin" value="$0" detail="Requires approval boundary" /></div>
            <div className="section-grid"><section className="panel"><p className="eyebrow">Revenue assurance</p><h2 className="section-title">Keep commercial context separate from realized value</h2><div className="value-lanes"><div><span>01</span><p><b>Confirmed contract value exposed</b><small>$420K · two assurance requests</small></p><Badge variant="outline">CONTEXT</Badge></div><div><span>02</span><p><b>Modeled pipeline influenced</b><small>$210K · probability weighted</small></p><Badge variant="outline">MODELED</Badge></div><div><span>03</span><p><b>Finance-approved attributable margin</b><small>$0 · pending causal approval</small></p><Badge variant="outline">ROI ELIGIBLE</Badge></div></div></section><section className="panel formula-panel"><p className="eyebrow">Defensible unit economics</p><h2 className="section-title">Value enters ROI only after verification</h2><code>cost / accepted evidence =<br />(collection + storage + model + review + rework)<br />÷ auditor-accepted artifacts</code><code>net verified value =<br />avoided labor + avoided rework + expected-loss reduction<br />+ approved margin − total cost</code><p className="guardrail"><ShieldCheck size={15} />Full contract value and influenced pipeline never enter ROI automatically.</p></section></div>
          </TabsContent>

          <TabsContent value="evolution" className="pt-6">
            <section className="panel evolution-panel"><div className="panel-heading"><div><p className="eyebrow">Closed-loop assurance</p><h2 className="section-title">Every production failure becomes a permanent test</h2></div><Badge className="live-badge"><RotateCcw /> Continuous</Badge></div><div className="loop-grid">{[['01','Observe','Incident, drift or near miss'],['02','Sanitize','Remove secrets and customer data'],['03','Evaluate','Deterministic + agentic regression'],['04','Shadow','Replay against production shape'],['05','Approve','GRC and control-owner boundary'],['06','Release','Progressive rollout + SLO watch']].map(([n,title,copy])=><article key={n}><span>{n}</span><Network /><b>{title}</b><p>{copy}</p></article>)}</div><div className="release-gate"><TimerReset /><div><b>Current release gate</b><span>64 regression assertions · 100% critical conflict detection · 99.9% replay target</span></div><Badge variant="outline">SHADOW</Badge></div></section>
          </TabsContent>
        </Tabs>
        <footer><span>Reference simulation · not a production claim or vendor ranking</span><span>OSCAL-aligned · tool-neutral · fail-closed</span></footer>
      </div>
    </main>
  );
}
