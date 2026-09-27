(define (problem blocksworld-problema)
  (:domain blocks)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear f)
    (clear d)
    (handempty)
    (on e b)
    (on f e)
    (on a c)
    (on d a)
    (ontable b)
    (ontable c)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
