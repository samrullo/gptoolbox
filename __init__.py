import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
import datetime
import pickle

app = Flask(__name__)


### Utilities ###
def convert_to_html(command_arr):
    command_arr[0] = '<span class="command_keyword">' + command_arr[0] + '</span>'
    for i in range(len(command_arr)):
        if command_arr[i][0] == '-':
            command_arr[i] = '<span class="command_switch">' + command_arr[i] + '</span>'
    command_html = " ".join(command_arr)
    return command_html


@app.route('/')
def render_main():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/interactive')
def interactive():
    return render_template('interactive.html')


@app.route('/query')
def render_queries():
    try:
        file = os.path.dirname(__file__)+'\\SQL_ABBREVIATIONS.xlsx'
        df = pd.read_excel(file)
        return render_template('sql_queries.html', result=df)
    except Exception as e:
        return str(e)


@app.route('/command_generator')
def render_command_generator():
    try:
        return render_template('command_generator.html')
    except Exception as e:
        return str(e)


@app.route('/cnc')
def render_cnc_generator():
    try:
        date = datetime.date.today()
        date_yyyymmdd = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
        if os.path.exists('cnc_args.dat'):
            cnc_args_file = open('cnc_args.dat', 'rb')
            cnc_args = pickle.load(cnc_args_file)
            cnc_args_file.close()
            return render_template('cnc_template.html', client=cnc_args['client'], package=cnc_args['package'],
                                   fund=cnc_args['fund'], date=cnc_args['date'], directory=cnc_args['directory'],
                                   tag='running cnc', report_tag=cnc_args['report_tag'],
                                   breakdown=cnc_args['breakdown'], depth=cnc_args['depth'])
        else:
            return render_template('cnc_template.html', date=date_yyyymmdd)
    except Exception as e:
        return str(e)


@app.route('/pms')
def render_pms_generator():
    try:
        if os.path.exists('pms_args.dat'):
            pms_args_file = open('pms_args.dat', 'rb')
            pms_args = pickle.load(pms_args_file)
            pms_args_file.close()
            return render_template('pms_template.html', client=pms_args['client'], package=pms_args['package'],
                                   fund=pms_args['fund'], date=pms_args['date'], directory=pms_args['directory'],
                                   tag='running scratch')
        else:
            return render_template('pms_template.html')
    except Exception as e:
        return str(e)


@app.route('/master_batcher')
def render_master_batcher_generator():
    try:
        date = datetime.date.today()
        date_yyyymmdd = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
        if os.path.exists('mb_args.dat'):
            mb_args_file = open('mb_args.dat', 'rb')
            mb_args = pickle.load(mb_args_file)
            mb_args_file.close()
            return render_template('master_batcher_template.html', client=mb_args['client'], package=mb_args['package'],
                                   date=mb_args['date'], px_hier=mb_args['px_hier'], rk_hier=mb_args['rk_hier'],
                                   tag='running price/risk', write_purpose=mb_args['write_purpose'],
                                   bcsettings=mb_args['bcsettings'], bcsettings_ver=mb_args['bcsettings_ver'])
        else:
            return render_template('master_batcher_template.html', date=date_yyyymmdd, px_hier='NAV', rk_hier='RISK',
                                   tag='running price/risk')
    except Exception as e:
        return str(e)


@app.route('/pkg_batcher')
def render_pkg_batcher_generator():
    try:
        date = datetime.date.today()
        date_yyyymmdd = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
        if os.path.exists('pkg_batcher_args.dat'):
            pkg_batcher_args_file = open('pkg_batcher_args.dat', 'rb')
            pkg_batcher_args = pickle.load(pkg_batcher_args_file)
            pkg_batcher_args_file.close()
            return render_template('pkg_batcher_template.html', client=pkg_batcher_args['client'],
                                   package=pkg_batcher_args['package'], date=pkg_batcher_args['date'],
                                   run=pkg_batcher_args['run'], sect=pkg_batcher_args['sect'],
                                   tag='running pkg_batcher', pg=pkg_batcher_args['pg'])
        else:
            return render_template('pkg_batcher_template.html', date=date_yyyymmdd, tag='running pkg_batcher')
    except Exception as e:
        return str(e)


@app.route('/praada')
def render_praada_generator():
    try:
        date = datetime.date.today()
        date_yyyymmdd = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
        if os.path.exists('praada_args.dat'):
            praada_args_file = open('praada_args.dat', 'rb')
            praada_args = pickle.load(praada_args_file)
            praada_args_file.close()
            return render_template('praada_template.html', client=praada_args['client'], package=praada_args['package'],
                                   date=praada_args['date'], start_date=praada_args['start_date'],
                                   end_date=praada_args['end_date'],pg_cusipfile=praada_args['pg_cusipfile'],
                                   px_hier=praada_args['px_hier'], rk_hier=praada_args['rk_hier'],
                                   rpt_tag_select=praada_args['rpt_tag_select'], breakdown=praada_args['breakdown'],
                                   tag='running praada/cra')
        else:
            return render_template('praada_template.html', date=date_yyyymmdd, tag='running praada/cra',
                                   start_date=date_yyyymmdd, px_hier='NAV', rk_hier='RISK')
    except Exception as e:
        return str(e)


@app.route('/pms_generator')
def pms_generator():
    try:
        command = request.args.get('command', '', type=str)
        client = request.args.get('client', '', type=str)
        client = client.upper()
        package = request.args.get('package', '', type=str)
        package = package.upper()
        fund_pg_select = request.args.get('fund_pg_select', '', type=str)
        fund = request.args.get('fund', '', type=str)
        if fund_pg_select != 'file':
            fund = fund.upper()
        date = request.args.get('date', '', type=str)
        directory = request.args.get('directory', '', type=str)
        tag = request.args.get('tag', '', type=str)
        sector = request.args.get('sector', '', type=str)
        rpt_tag = request.args.get('rpt_tag', '', type=str)
        pms_args_file = open('pms_args.dat', 'wb')
        pms_args = {'client': client, 'package': package, 'fund': fund, 'date': date, 'directory': directory,
                    'tag': tag}
        pickle.dump(pms_args, pms_args_file)
        pms_args_file.close()
        if command == 'generic_pms':
            pms_template = """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """
            # pms_template="""pms_batch.pl <span class="command_switch">-{fund_pg_select}</span> {fund} <span class="command_switch">-cmd</span> "{date} <span class="command_switch">-gpsettings</span> GP:DAILY <span class="command_switch">-ignorePublish</span>" <span class="command_switch">-pkg</span> {pkg} <span class="command_switch">-dir</span> {directory} <span class="command_switch">-tag</span> "running scratch " """
            pms = pms_template.format(fund_pg_select=fund_pg_select, fund=fund, date=date, pkg=package,
                                      directory=directory, tag=tag)
            pms = pms.strip()
            pms_arr = pms.split()
            pms_html = convert_to_html(pms_arr)
            return jsonify(result=pms_html)
        elif command == 'compl_pms':
            #            pms_template="""pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -complBin -gpsettings GP:DAILY -complBin -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """
            pms_template = """ startPCS.pl {fund} {date} -loadProdGroups -gpsettings GP:BINARY -pkg {package} -complBin -ignorePublish """
            pms = pms_template.format(fund_pg_select=fund_pg_select, fund=fund, date=date, pkg=package,
                                      directory=directory, tag=tag)
            pms_arr = pms.split()
            pms_html = convert_to_html(pms_arr)
            return jsonify(result=pms_html)
        elif command == 'exposure_pms':
            pms_template = """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -save_exposure -save_exp_purpose P100 -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """
            pms = pms_template.format(fund_pg_select=fund_pg_select, fund=fund, date=date, pkg=package,
                                      directory=directory, tag=tag)
            pms_arr = pms.split()
            pms_html = convert_to_html(pms_arr)
            return jsonify(result=pms_html)
        elif command == 'sector_pms':
            pms_template = """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -writeSectorMap {sector} -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """
            pms = pms_template.format(fund_pg_select=fund_pg_select, fund=fund, date=date, pkg=package,
                                      directory=directory, tag=tag, sector=sector)
            pms_arr = pms.split()
            pms_html = convert_to_html(pms_arr)
            return jsonify(result=pms_html)
        elif command == 'port_totals':
            pms_template = """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -saveTotals {rpt_tag} -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """
            pms = pms_template.format(fund_pg_select=fund_pg_select, fund=fund, date=date, pkg=package,
                                      directory=directory, tag=tag, rpt_tag=rpt_tag)
            pms_arr = pms.split()
            pms_html = convert_to_html(pms_arr)
            return jsonify(result=pms_html)
        elif command == 'composite_bench_pms':
            pms_template = """pms_batch.pl -{fund_pg_select} {fund} -cmd "{date} -gpsettings GP:DAILY:i -benchmark -loadProdGroups -W {rpt_tag}.{sector} -ignorePublish" -pkg {pkg} -dir {directory} -tag "{tag}" """
            pms = pms_template.format(fund_pg_select=fund_pg_select, fund=fund, date=date, pkg=package,
                                      directory=directory, tag=tag, rpt_tag=rpt_tag, sector=sector)
            pms_arr = pms.split()
            pms_html = convert_to_html(pms_arr)
            return jsonify(result=pms_html)
    except Exception as e:
        return jsonify(result=str(e))


@app.route('/cnc_generator')
def cnc_generator():
    try:
        command = request.args.get('command', '', type=str)
        client = request.args.get('client', '', type=str)
        client = client.upper()
        package = request.args.get('package', '', type=str)
        package = package.upper()
        fund_pg_select = request.args.get('fund_pg_select', '', type=str)
        fund = request.args.get('fund', '', type=str)
        if fund_pg_select != 'file':
            fund = fund.upper()
        date = request.args.get('date', '', type=str)
        directory = request.args.get('directory', '', type=str)
        tag = request.args.get('tag', '', type=str)
        report_tag = request.args.get('report_tag', '', type=str)
        breakdown = request.args.get('breakdown', '', type=str)
        depth = request.args.get('depth', '', type=str)
        cnc_args_file = open('cnc_args.dat', 'wb')
        cnc_args = {'client': client, 'package': package, 'fund': fund, 'date': date, 'directory': directory,
                    'tag': tag, 'report_tag': report_tag, 'breakdown': breakdown, 'depth': depth}
        pickle.dump(cnc_args, cnc_args_file)
        cnc_args_file.close()
        # var related switches
        exp_hi = request.args.get('exp_hi', '', type=str)
        var_type = request.args.get('var_type', '', type=str)
        var_history = request.args.get('var_history', '', type=str)
        var_history_count = request.args.get('var_history_count', '', type=str)
        var_decay_daily = request.args.get('var_decay_daily', '', type=str)
        var_calendar = request.args.get('var_calendar', '', type=str)
        var_mat_date = request.args.get('var_mat_date', '', type=str)
        econ_date = request.args.get('econ_date', '', type=str)

        if command == 'generic_cnc':
            cnc_template = """ cnc_batch.pl -{fund_pg_select} {fund} -cmd "{date} -fund_level 10 -mid_level_funds -show_ticker -fund_html_rpt gp -fund_htlink_dir . -W {report_tag}.{breakdown}" -tag "{tag}" -dir {directory} -pkg {package} """
            cnc = cnc_template.format(fund_pg_select=fund_pg_select, fund=fund, date=date, report_tag=report_tag,
                                      breakdown=breakdown.upper(), tag=tag, directory=directory, package=package)
            cnc_arr = cnc.split()
            cnc_html = convert_to_html(cnc_arr)
            return jsonify(result=cnc_html)
        elif command == 'ifile_parse':
            if depth != '':
                iparse_template = """ifile_parse.pl -rpt {report_tag} -bd {breakdown} -depth {depth} -cnc -db -client {client} -client_tree {client_tree} -pkg {package} > /d0/prod1/reports/test/{report_tag}_{breakdown}.ifile"""
                iparse = iparse_template.format(client=client, client_tree=client, report_tag=report_tag,
                                                breakdown=breakdown, depth=depth, package=package)
            else:
                iparse_template = """ifile_parse.pl -rpt {report_tag} -bd {breakdown} -cnc -db -client {client} -client_tree {client_tree} -pkg {package} > /d0/prod1/reports/test/{report_tag}_{breakdown}.ifile"""
                iparse = iparse_template.format(client=client, client_tree=client, report_tag=report_tag,
                                                breakdown=breakdown, package=package)
            iparse_arr = iparse.split()
            iparse_html = convert_to_html(iparse_arr)
            return jsonify(result=iparse_html)
        elif command == 'cnc_custom_var':
            cnc_custom_var_template = """
            :mid_level_funds Y
            :no_pg_html Y
            :enable_gppos_link Y
            :use_brk_title Y            
            :fund_htlink_dir .
            :show_all_sectors N
            :show_ticker Y
            :fund_level 10
            :suppress_cash_no_short Y
            :load_port_risk Y
            :var_use_gp N
            :exp_hi {exp_hi}
            :var_type {var_type}
            :{var_history} {var_history_count}
            :var_decay_daily {var_decay_daily}
            :var_calendar {var_calendar}
            W smi_var_99_10day_sum
            :var_mat_date {var_mat_date}
            :econ_date {econ_date}
            W smi_svar_99_10day            
            """
            cnc_custom_var = cnc_custom_var_template.format(exp_hi=exp_hi, var_type=var_type, var_history=var_history,
                                                            var_history_count=var_history_count,
                                                            var_decay_daily=var_decay_daily, var_calendar=var_calendar,
                                                            var_mat_date=var_mat_date, econ_date=econ_date)
            return jsonify(result=cnc_custom_var)
    except Exception as e:
        return jsonify(result=str(e))


@app.route('/master_batcher_generator')
def master_batcher_generator():
    try:
        command = request.args.get('command', '', type=str)
        client = request.args.get('client', '', type=str)
        client = client.upper()
        package = request.args.get('package', '', type=str)
        package = package.upper()
        pg_cusip_select = request.args.get('pg_cusip_select', '', type=str)
        pg_cusip_file = request.args.get('pg_cusip_file', '', type=str)
        if pg_cusip_file == 'pg':
            pg_cusip_file = pg_cusip_file.upper()
        date = request.args.get('date', '', type=str)
        px_hier = request.args.get('px_hier', '', type=str)
        rk_hier = request.args.get('rk_hier', '', type=str)
        rk_run_type = request.args.get('rk_run_type', '', type=str)
        bcsettings = request.args.get('bcsettings', '', type=str)
        bcsettings_ver = request.args.get('bcsettings_ver', '', type=str)
        write_purpose = request.args.get('write_purpose', '', type=str)
        tag = request.args.get('tag', '', type=str)
        mb_args_file = open('mb_args.dat', 'wb')
        mb_args = {'client': client, 'package': package, 'date': date, 'px_hier': px_hier, 'rk_hier': rk_hier,
                   'bcsettings': bcsettings, 'bcsettings_ver': bcsettings_ver, 'write_purpose': write_purpose,
                   'tag': tag}
        pickle.dump(mb_args, mb_args_file)
        mb_args_file.close()
        if command == 'price':
            if write_purpose != '':
                if bcsettings != '' and bcsettings_ver != '':
                    price_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M BOGUS -D BOGUS -r SPDPX -m -1 -cus_tol 0 -pri 9000 -tag '{tag}' -write_purpose {write_purpose} -bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver}"""
                    price = price_template.format(date=date, package=package, client=client,
                                                  pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file, tag=tag,
                                                  write_purpose=write_purpose, bcsettings=bcsettings,
                                                  bcsettings_ver=bcsettings_ver)
                elif bcsettings_ver != '':
                    price_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M BOGUS -D BOGUS -r SPDPX -m -1 -cus_tol 0 -pri 9000 -tag '{tag}' -write_purpose {write_purpose} -bcsettings_ver {bcsettings_ver}"""
                    price = price_template.format(date=date, package=package, client=client,
                                                  pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file, tag=tag,
                                                  write_purpose=write_purpose, bcsettings_ver=bcsettings_ver)
                else:
                    price_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -log log -pkg {package} -client {client} -{pg_cusip_select} {cusip_file} -M BOGUS -D BOGUS -r SPDPX -m -1 -cus_tol 0 -pri 9000 -tag '{tag}' -write_purpose {write_purpose}"""
                    price = price_template.format(date=date, package=package, client=client,
                                                  pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file, tag=tag,
                                                  write_purpose=write_purpose)
            else:
                if bcsettings != '' and bcsettings_ver != '':
                    price_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M BOGUS -D BOGUS -r SPDPX -m -1 -cus_tol 0 -pri 9000 -tag '{tag}' -bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver}"""
                    price = price_template.format(date=date, package=package, client=client,
                                                  pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file, tag=tag,
                                                  bcsettings=bcsettings, bcsettings_ver=bcsettings_ver)
                elif bcsettings_ver != '':
                    price_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M BOGUS -D BOGUS -r SPDPX -m -1 -cus_tol 0 -pri 9000 -tag '{tag}' -bcsettings_ver {bcsettings_ver}"""
                    price = price_template.format(date=date, package=package, client=client,
                                                  pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file, tag=tag,
                                                  bcsettings_ver=bcsettings_ver)
                else:
                    price_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M BOGUS -D BOGUS -r SPDPX -m -1 -cus_tol 0 -pri 9000 -tag '{tag}' """
                    price = price_template.format(date=date, package=package, client=client,
                                                  pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file, tag=tag)
            price_arr = price.split()
            price_html = convert_to_html(price_arr)
            return jsonify(result=price_html)
        elif command == 'oas_price':
            if write_purpose != '':
                if bcsettings != '' and bcsettings_ver != '':
                    price_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver} " -mno 250 -r OAV -p {write_purpose} -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    price = price_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings=bcsettings,
                                                  bcsettings_ver=bcsettings_ver, tag=tag, client=client,
                                                  package=package, write_purpose=write_purpose)
                elif bcsettings_ver != '':
                    price_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver {bcsettings_ver} " -mno 250 -r OAV -p {write_purpose} -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    price = price_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                  tag=tag, client=client, package=package, write_purpose=write_purpose)
                else:
                    price_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver PROD " -mno 250 -r OAV -p {write_purpose} -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    price = price_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                  tag=tag, client=client, package=package, write_purpose=write_purpose)
            else:
                if bcsettings != '' and bcsettings_ver != '':
                    price_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver} " -mno 250 -r OAV -p OAV -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    price = price_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings=bcsettings,
                                                  bcsettings_ver=bcsettings_ver, tag=tag, client=client,
                                                  package=package)
                elif bcsettings_ver != '':
                    price_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver {bcsettings_ver} " -mno 250 -r OAV -p OAV -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    price = price_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                  tag=tag, client=client, package=package)
                else:
                    price_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver PROD " -mno 250 -r OAV -p OAV -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    price = price_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                  tag=tag, client=client, package=package)
            price_arr = price.split()
            price_html = convert_to_html(price_arr)
            return jsonify(result=price_html)
        elif command == 'risk':
            if write_purpose != '':
                if bcsettings != '' and bcsettings_ver != '':
                    risk_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -run {rk_run_type} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M {px_hier} -D {rk_hier} -cus_tol  30 -pri  9000 -mno  200 -ignore_pricing_cusip -bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver} -write_purpose {write_purpose}"""
                    risk = risk_template.format(date=date, rk_run_type=rk_run_type, package=package, client=client,
                                                pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file,
                                                px_hier=px_hier, rk_hier=rk_hier, bcsettings=bcsettings,
                                                bcsettings_ver=bcsettings_ver, write_purpose=write_purpose)
                elif bcsettings_ver != '':
                    risk_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -run {rk_run_type} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M {px_hier} -D {rk_hier} -cus_tol  30 -pri  9000 -mno  200 -ignore_pricing_cusip -bcsettings_ver {bcsettings_ver} -write_purpose {write_purpose}"""
                    risk = risk_template.format(date=date, rk_run_type=rk_run_type, package=package, client=client,
                                                pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file,
                                                px_hier=px_hier, rk_hier=rk_hier, bcsettings_ver=bcsettings_ver,
                                                write_purpose=write_purpose)
                else:
                    risk_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -run {rk_run_type} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M {px_hier} -D {rk_hier} -cus_tol  30 -pri  9000 -mno  200 -ignore_pricing_cusip -write_purpose {write_purpose}"""
                    risk = risk_template.format(date=date, rk_run_type=rk_run_type, package=package, client=client,
                                                pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file,
                                                px_hier=px_hier, rk_hier=rk_hier, write_purpose=write_purpose)
            else:
                if bcsettings != '' and bcsettings_ver != '':
                    risk_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -run {rk_run_type} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M {px_hier} -D {rk_hier} -cus_tol  30 -pri  9000 -mno  200 -ignore_pricing_cusip -bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver}"""
                    risk = risk_template.format(date=date, rk_run_type=rk_run_type, package=package, client=client,
                                                pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file,
                                                px_hier=px_hier, rk_hier=rk_hier, bcsettings=bcsettings,
                                                bcsettings_ver=bcsettings_ver)
                elif bcsettings_ver != '':
                    risk_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -run {rk_run_type} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M {px_hier} -D {rk_hier} -cus_tol  30 -pri  9000 -mno  200 -ignore_pricing_cusip -bcsettings_ver {bcsettings_ver}"""
                    risk = risk_template.format(date=date, rk_run_type=rk_run_type, package=package, client=client,
                                                pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file,
                                                px_hier=px_hier, rk_hier=rk_hier, bcsettings_ver=bcsettings_ver)
                else:
                    risk_template = """ master_batcher.pl -mb /usr/local/bfm/std/GreenPkg/DREAM.mb -a {date} -run {rk_run_type} -log log -pkg {package} -client {client} -{pg_cusip_select} {pg_cusip_file} -M {px_hier} -D {rk_hier} -cus_tol  30 -pri  9000 -mno  200 -ignore_pricing_cusip """
                    risk = risk_template.format(date=date, rk_run_type=rk_run_type, package=package, client=client,
                                                pg_cusip_select=pg_cusip_select, pg_cusip_file=pg_cusip_file,
                                                px_hier=px_hier, rk_hier=rk_hier)
            risk_arr = risk.split()
            risk_html = convert_to_html(risk_arr)
            return jsonify(result=risk_html)
        elif command == 'oas_risk':
            if write_purpose != '':
                if bcsettings != '' and bcsettings_ver != '':
                    risk_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver} " -mno 250 -r {rk_run_type} -p {write_purpose} -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    risk = risk_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings=bcsettings,
                                                bcsettings_ver=bcsettings_ver, tag=tag, client=client, package=package,
                                                rk_run_type=rk_run_type, write_purpose=write_purpose)
                elif bcsettings_ver != '':
                    risk_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver {bcsettings_ver} " -mno 250 -r {rk_run_type} -p {write_purpose} -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    risk = risk_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                tag=tag, client=client, package=package, rk_run_type=rk_run_type,
                                                write_purpose=write_purpose)
                else:
                    risk_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver PROD " -mno 250 -r {rk_run_type} -p {write_purpose} -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    risk = risk_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                tag=tag, client=client, package=package, rk_run_type=rk_run_type,
                                                write_purpose=write_purpose)
            else:
                if bcsettings != '' and bcsettings_ver != '':
                    risk_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings {bcsettings} -bcsettings_ver {bcsettings_ver} " -mno 250 -r {rk_run_type} -p P100 -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    risk = risk_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings=bcsettings,
                                                bcsettings_ver=bcsettings_ver, rk_run_type=rk_run_type, tag=tag,
                                                client=client, package=package)
                elif bcsettings_ver != '':
                    risk_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver {bcsettings_ver} " -mno 250 -r {rk_run_type} -p P100 -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    risk = risk_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                rk_run_type=rk_run_type, tag=tag, client=client, package=package)
                else:
                    risk_template = """ OasBatch -c {pg_cusip_file} -a {date} -extraArgs "\-bcsettings DEFAULT,WEEKEND -bcsettings_ver PROD " -mno 250 -r {rk_run_type} -p P100 -s BRS -tag "{tag}" -client {client} -package {package} -program BondCalc """
                    risk = risk_template.format(pg_cusip_file=pg_cusip_file, date=date, bcsettings_ver=bcsettings_ver,
                                                rk_run_type=rk_run_type, tag=tag, client=client, package=package)
            risk_arr = risk.split()
            risk_html = convert_to_html(risk_arr)
            return jsonify(result=risk_html)
    except Exception as e:
        return jsonify(result=str(e))


@app.route('/pkg_batcher_generator')
def pkg_batcher_generator():
    try:
        command = request.args.get('command', '', type=str)
        client = request.args.get('client', '', type=str)
        client = client.upper()
        package = request.args.get('package', '', type=str)
        package = package.upper()
        pcl = request.args.get('pcl', '', type=str)
        pcl = pcl.upper()
        run_select = request.args.get('run_select', '', type=str)
        run_select = run_select.upper()
        run = request.args.get('run', '', type=str)
        run = run.upper()
        sect = request.args.get('sect', '', type=str)
        sect = sect.upper()
        date = request.args.get('date', '', type=str)
        pg = request.args.get('pg', '', type=str)
        tag = request.args.get('tag', '', type=str)
        pkg_batcher_args_file = open('pkg_batcher_args.dat', 'wb')
        pkg_batcher_args = {'client': client, 'package': package, 'date': date,
                            'run_select': run_select, 'run': run, 'sect': sect, 'pg': pg, 'tag': tag}
        pickle.dump(pkg_batcher_args, pkg_batcher_args_file)
        pkg_batcher_args_file.close()
        if command == 'pkg_batcher_run_select':
            pkg_batcher_template = """ pkg_batcher.pl -a {date} -pkg {package} -pcl {client}::{pcl}.pcl -run {run_select} -log pikachu """
            pkg_batcher = pkg_batcher_template.format(date=date, package=package, client=client, pcl=pcl,
                                                      run_select=run_select)
        elif command == "pkg_batcher_run":
            pkg_batcher_template = """ pkg_batcher.pl -a {date} -pkg {package} -pcl {client}::{pcl}.pcl -run {run} -sect {sect} -log pikachu """
            pkg_batcher = pkg_batcher_template.format(date=date, package=package, client=client, pcl=pcl, run=run,
                                                      sect=sect)
        elif command == 'agg_all':
            pkg_batcher_template = """ /usr/local/bfm/etc/index/AggAllWrapper.pl -pg {pg} -date {date} -force """
            pkg_batcher = pkg_batcher_template.format(pg=pg, date=date)
        elif command == 'dream_covers':
            pkg_batcher_template = """ pkg_batcher.pl -a {date} -gp -pkg {package} -pcl /usr/local/bfm/std/GreenPkg/DREAM.pcl -run AGGREGATE -sect LIST,PROD,DRPATCH -log DREAM_LIST -client {client} """
            pkg_batcher = pkg_batcher_template.format(date=date, package=package, client=client)
        elif command == 'dream_release':
            pkg_batcher_template = """ pkg_batcher.pl -a {date} -gp -pkg {package} -pcl /usr/local/bfm/std/GreenPkg/DREAM.pcl -run RELEASE -log DREAM_LIST -client {client} """
            pkg_batcher = pkg_batcher_template.format(date=date, package=package, client=client)
        pkg_batcher_arr = pkg_batcher.split()
        pkg_batcher_html = convert_to_html(pkg_batcher_arr)
        return jsonify(result=pkg_batcher_html)
    except Exception as e:
        return jsonify(result=str(e))


@app.route('/praada_generator')
def praada_generator():
    try:
        command = request.args.get('command', '', type=str)
        client = request.args.get('client', '', type=str)
        client = client.upper()
        package = request.args.get('package', '', type=str)
        package = package.upper()
        date = request.args.get('date', '', type=str)
        start_date = request.args.get('start_date', '', type=str)
        end_date = request.args.get('end_date', '', type=str)
        pg_cusipfile_select = request.args.get('pg_cusipfile_select', '', type=str)
        pg_cusipfile = request.args.get('pg_cusipfile', '', type=str)
        if pg_cusipfile_select == 'pg':
            pg_cusipfile = pg_cusipfile.upper()
        rpt_tag_select = request.args.get('rpt_tag_select', '', type=str)
        breakdown = request.args.get('breakdown', '', type=str)
        px_hier = request.args.get('px_hier', '', type=str)
        rk_hier = request.args.get('rk_hier', '', type=str)
        directory = request.args.get('directory', '', type=str)
        tag = request.args.get('tag', '', type=str)
        praada_args_file = open('praada_args.dat', 'wb')
        praada_args = {'client': client, 'package': package, 'date': date,
                       'start_date': start_date, 'end_date': end_date,
                       'pg_cusipfile': pg_cusipfile, 'px_hier': px_hier,
                       'rk_hier': rk_hier, 'directory': directory, 'rpt_tag_select': rpt_tag_select,
                       'breakdown': breakdown, 'tag': tag}
        pickle.dump(praada_args, praada_args_file)
        praada_args_file.close()
        print('praada_nav command is ', command)
        if command == 'praada_nav':
            praada_template = """ praada_nav.pl -port {pg_cusipfile} -start_date {start_date} -run_category DAILY -pkg {package} -rptdir {directory}  -W {rpt_tag_select}.{breakdown} -service BATCH -gpsettings GP """
            praada = praada_template.format(pg_cusipfile=pg_cusipfile, start_date=start_date, package=package,
                                            directory=directory, rpt_tag_select=rpt_tag_select, breakdown=breakdown)
            print('praada_nav command is ', praada)
        elif command == 'praada_nav_no_blob':
            praada_template = """ praada_nav.pl  -port {pg_cusipfile} -end {end_date} -pkg_date {date} -ph {px_hier} -rh {rk_hier} -gpsettings GP -rptdir {directory} -run_category DAILY -pkg_lag 300 -pkg {package}  -W {rpt_tag_select}.{breakdown} -service BATCH -reporting_mode DETAIL -multi_period NOBLOB -run_from_scratch """
            praada = praada_template.format(pg_cusipfile=pg_cusipfile, end_date=end_date, date=date, px_hier=px_hier,
                                            rk_hier=rk_hier, package=package, directory=directory,
                                            rpt_tag_select=rpt_tag_select, breakdown=breakdown)
        elif command == 'cra_wrapper_cra':
            praada_template = """ cra_wrapper.pl  -date {date} -gp -pkg {package} -pg {pg_cusipfile} -gpsettings GP:DAILY -tca """
            praada = praada_template.format(pg_cusipfile=pg_cusipfile, date=date, package=package)
        elif command == 'cra_wrapper_praada':
            praada_template = """ cra_wrapper.pl  -date {date} -gp -pkg {package} -pg {pg_cusipfile} -gpsettings GP:DAILY -no_cra -praada -reporting_mode DETAIL """
            praada = praada_template.format(pg_cusipfile=pg_cusipfile, date=date, package=package)
        elif command == 'cra_date_looper':
            praada_template = """ date_looper.pl -run "cra -file {pg_cusipfile} -log -mode all -purpose RETATT -save -ph {px_hier} -rh {rk_hier} " -date_tag "date {start_date} {end_date}" -days """
            praada = praada_template.format(pg_cusipfile=pg_cusipfile, px_hier=px_hier, rk_hier=rk_hier,
                                            start_date=start_date, end_date=end_date)
        praada_arr = praada.split()
        praada_html = convert_to_html(praada_arr)
        return jsonify(result=praada_html)
    except Exception as e:
        return jsonify(result=str(e))


if __name__ == '__main__':
    app.run()
