"""Local browser interface. Keys remain in Python, never in browser fields."""
from pathlib import Path
import streamlit as st
from common import ROOT, read
from desk import parser, run

st.set_page_config(page_title='Equity Research Desk', page_icon='📊', layout='wide')
st.markdown('''<style>
.stApp {background:#f5f5f0;color:#172c2a} h1,h2,h3 {font-family:Georgia,serif}
[data-testid="stMetric"] {background:white;padding:18px;border:1px solid #d4ddd5;border-radius:8px}
</style>''',unsafe_allow_html=True)
st.caption('MASTERING AI FOR FINANCE  /  CHECKPOINT 2')
st.title('Equity Research Desk')
st.write('Read the filings. Follow the analysis. Check the evidence.')
mode=st.radio('Work mode',['Saved report review (offline)','Agent team (API required)'],horizontal=True)
if mode=='Saved report review (offline)':
    from offline_audit import review
    st.info('Offline mode checks the eleven core claims in a saved fallback report. It makes no API calls. Period and definition checks by a model remain pending.')
    left,right=st.columns([1,2],gap='large')
    with left:
        st.subheader('Saved source set')
        sources=sorted((ROOT/'runs').glob('*_sources'),reverse=True)
        source=st.selectbox('Company and saved filings',sources,format_func=lambda p:p.name.split('_')[0],index=0 if sources else None)
        if source:
            data=read(source/'bundle.json')
            st.write('Annual period:',data['filings']['annual']['period_end'])
            st.write('Earnings release:',data['filings']['earnings']['filing_date'])
            st.write('Supplied close:',f"${data['price']:,.2f}", 'on',data['price_date'])
            st.caption('Price source: '+data['price_source']+'. Source verification remains pending.')
            if st.button('Run offline checks',type='primary',width='stretch'):
                with st.spinner('Checking saved facts and arithmetic…'):
                    folder=review(source)
                    st.session_state['offline_folder']=str(folder)
        st.caption('Saved source files stay unchanged. Each review creates a new folder.')
    with right:
        st.subheader('Offline numerical review')
        chosen=st.session_state.get('offline_folder')
        if chosen and (Path(chosen)/'offline-report.md').exists():
            folder=Path(chosen);marks=read(folder/'offline-marks.json')['marks']
            cols=st.columns(3)
            for col,mark in zip(cols,['code correct','wrong','unsupported']):
                col.metric(mark.title(),sum(m['code_mark']==mark for m in marks))
            text=(folder/'offline-report.md').read_text()
            st.download_button('Download offline review',text,file_name=folder.name+'-offline.md')
            st.markdown(text)
        else:
            st.write('Select a saved source set and run the checks to see the evidence table and report.')
    with st.expander('Seeded-error evidence'):
        p=ROOT/'offline-proof-results.json'
        if p.exists():
            result=read(p)
            st.write(result['mode'])
            rows=[{'Trial':label,**values['marks']} for label,values in result['results'].items()]
            st.dataframe(rows,hide_index=True,width='stretch')
            st.caption('These are code-only results. They are not the complete model-backed Checkpoint 2 proof.')
    st.caption('This is a learning exercise, not financial advice. AI assistance: OpenAI Codex; Python. Human verification remains pending.')
    st.stop()

left,right=st.columns([1,2],gap='large')
with left:
    st.subheader('Start a research run')
    with st.form('research'):
        provider=st.selectbox('Model provider',['anthropic','openai'],format_func=lambda p:'Anthropic Claude' if p=='anthropic' else 'OpenAI')
        ticker=st.text_input('Company ticker',placeholder='Enter a U.S. listed ticker').strip().upper()
        peers=st.text_input('Peer tickers (optional)',placeholder='Separate tickers with commas').strip().upper()
        price=st.number_input('Closing price (optional; 0 omits it)',min_value=0.0,step=0.01,format='%.2f')
        price_date=st.date_input('Price date')
        price_source=st.text_input('Price source',placeholder='Source name or URL')
        saved=st.selectbox('Filing source',['Retrieve latest SEC filings','Use a saved source set'])
        folders=sorted([p for p in (ROOT/'runs').glob('*') if (p/'bundle.json').exists()],reverse=True)
        source=st.selectbox('Saved source set',folders,format_func=lambda p:p.name,index=0 if folders else None)
        submitted=st.form_submit_button('Run research',type='primary',width='stretch')
    st.caption('Every completed research run includes the Verifier. Prices you enter are assumptions until you check their source.')
with right:
    st.subheader('Research and verification')
    if submitted:
        if not ticker:
            st.error('Enter a ticker.')
        elif price and not price_source:
            st.error('Enter a source for the price.')
        elif saved=='Use a saved source set' and source is None:
            st.error('There are no saved source sets yet. Retrieve the latest filings first.')
        else:
            args=parser().parse_args([ticker])
            args.provider=provider
            args.peers=peers;args.price=price or None
            args.price_date=price_date.isoformat() if price else None
            args.price_source=price_source if price else None
            args.source_run=source if saved=='Use a saved source set' else None
            with st.status('Running the research desk…',expanded=True) as status:
                try:
                    folder=run(args,emit=st.write)
                    st.session_state['report_folder']=str(folder)
                    status.update(label='Research and verification complete',state='complete')
                except Exception as exc:
                    status.update(label='Run stopped',state='error')
                    st.error(f'{type(exc).__name__}: '+str(exc)[:300])
    chosen=st.session_state.get('report_folder')
    if chosen and (Path(chosen)/'verified-report.md').exists():
        folder=Path(chosen)
        marks=read(folder/'verifier-marks.json')['marks']
        cols=st.columns(3)
        for col,mark in zip(cols,['correct','wrong','unsupported']):
            col.metric(mark.title(),sum(m['mark']==mark for m in marks))
        text=(folder/'verified-report.md').read_text()
        st.download_button('Download verified report',text,file_name=folder.name+'-verified.md')
        st.markdown(text)
    else:
        st.info('Start a run to see each node as it executes, followed by the report and verifier marks.')
st.divider()
with st.expander('Open a completed report'):
    completed=sorted([p for p in (ROOT/'runs').glob('*') if (p/'verified-report.md').exists()],reverse=True)
    selected=st.selectbox('Completed run',completed,format_func=lambda p:p.name,index=0 if completed else None)
    if selected and st.button('Read report'):
        st.session_state['report_folder']=str(selected);st.rerun()
st.caption('This is a learning exercise, not financial advice. AI assistance: OpenAI Codex and OpenAI API. Human source verification remains separate.')
