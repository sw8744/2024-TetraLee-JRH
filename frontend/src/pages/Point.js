import Header from './Header';
import { useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CJOne from './points/CJOne.png';
import HappyPoint from './points/HappyPoint.png';
import HPoint from './points/HPoint.png';
import LPoint from './points/LPoint.png';
import OKCashbag from './points/OKCashbag.jpg';
import SinsegaePoint from './points/SinsegaePoint.png';
import './Point.css';
import getSpeech from '../util/GetSpeech';

function Point() {
    const [searchParams] = useSearchParams();
    const [whereToEat, setWhereToEat] = useState('');
    const id = searchParams.get('id');
    const navigate = useNavigate();

    const fetchId = async () => {
        await fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
        });
    };

    const pay = () => {
        navigate('/pay?id=' + id);
    }

    const cancel = () => {
        navigate('/howtopay?id=' + id);
    };

    useEffect(() => {
        fetchId();
        getSpeech('포인트 적립을 시작합니다.')
    }, []);

  return (
    <>
      <Header whereToEat={whereToEat} />
      <div className='pointInfoDiv'>
        <p className='pointInfoTitle'>포인트 적립</p>
        <p className='pointInfoSubtitle'>어느 포인트를 적립하시겠습니까?</p>
      </div>
      <div className='pointSelectorDiv'>
        <div className='pointSelector'>
          <button className='pointButton' onClick={() => {pay()}}><img className='pointImg' src={CJOne} /><br/>CJ ONE</button>
          <button className='pointButton' onClick={() => {pay()}}><img className='pointImg' src={HappyPoint} /><br/>해피포인트</button>
          <button className='pointButton' onClick={() => {pay()}}><img className='pointImg' src={HPoint} /><br/>H.POINT</button>
        </div>
        <div className='pointSelector'>
          <button className='pointButton' onClick={() => {pay()}}><img className='pointImg' src={LPoint} /><br/>L POINT</button>
          <button className='pointButton' onClick={() => {pay()}}><img className='pointImg' src={OKCashbag} /><br/>OK 캐쉬백</button>
          <button className='pointButton' onClick={() => {pay()}}><img className='pointImg' src={SinsegaePoint} /><br/>신세계포인트</button>
        </div>
      </div>
      <footer className='footer4'>
        <button className='cancelButton4' onClick={() => {cancel()}}>이전으로</button>
      </footer>
    </>
  )
}

export default Point;