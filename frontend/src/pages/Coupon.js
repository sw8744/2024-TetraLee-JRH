import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import Header from "./Header";
import './Coupon.css';
import getSpeech from "../util/GetSpeech";

function Coupon() {
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
        getSpeech('쿠폰을 단말기에 인식시켜 주세요.')
    }, []);

    return (
        <>
            <Header whereToEat={whereToEat}/>
            <p className='couponInfoTitle'>포인트 적립</p>
            <div className="couponInfoDiv">
                <p className="couponInfo">쿠폰을 단말기에 인식시켜 주세요.</p>
                <p className="couponReaderInfo">단말기는 오른쪽 하단에 위치하여 있습니다.</p>
            </div>
            <button className="recognizeButton" onClick={() => {pay()}}>인식하기</button>
        </>
    );
}

export default Coupon;